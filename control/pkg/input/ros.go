package input

import (
	"fmt"
	"github.com/aler9/goroslib"
	"github.com/aler9/goroslib/pkg/msgs/std_srvs"
	"github.com/aler9/goroslib/pkg/msgs/sensor_msgs"
	"github.com/gwaxG/robot_ws/control/pkg/connections"
	"github.com/gwaxG/robot_ws/control/pkg/state"
	"github.com/gwaxG/robot_ws/control/pkg/utils"
	"math"
)

var Flippers      bool
var Arm           bool
	
type Ros struct {
	stateChange chan state.State
	state       state.State
	reset       chan bool
}

func (r *Ros) Init(stateChange chan state.State, reset chan bool) {
	r.reset = reset
	r.stateChange = stateChange
	r.state = state.State{}
}

func (r *Ros) Serve() {
	var err error
	var subBase *goroslib.Subscriber
	var subJoy *goroslib.Subscriber
	var servReset *goroslib.ServiceProvider

	subBase, err = goroslib.NewSubscriber(goroslib.SubscriberConf{
		Node:     connections.RosConnection(),
		Topic:    "robot_cmd",
		Callback: r.onRequest,
	})
	
	subJoy, err = goroslib.NewSubscriber(goroslib.SubscriberConf{
		Node:     connections.RosConnection(),
		Topic:    "joy",
		Callback: r.JoyCallback,
	})
	
	utils.FailOnError(err, "Failed to create platform_cmd subscriber")
	defer func() { err = subBase.Close(); utils.FailOnError(err, "Failed to disconnect from robot_cmd") }()
	defer func() { err = subJoy.Close(); utils.FailOnError(err, "Failed to disconnect from joy") }()

	servReset, err = goroslib.NewServiceProvider(goroslib.ServiceProviderConf{
		Node:     connections.RosConnection(),
		Name:     "robot/reset",
		Srv:      &std_srvs.Trigger{},
		Callback: r.onResetService,
	})
	utils.FailOnError(err, "Failed to create platform_cmd subscriber")
	defer func() { err = servReset.Close(); utils.FailOnError(err, "Failed to disconnect from reset service") }()

	select {}
}

func (r *Ros) onResetService(_ *std_srvs.TriggerReq) *std_srvs.TriggerRes {
	r.reset <- true
	return &std_srvs.TriggerRes{
		Success: true,
		Message: "Request handled",
	}
}

func (r *Ros) onRequest(msg *state.State) {
	r.state.Linear = msg.Linear
	r.state.Angular = msg.Angular
	r.state.FrontFlippers = msg.FrontFlippers
	r.state.RearFlippers = msg.RearFlippers
	r.state.ArmJoint1 = msg.ArmJoint1
	r.state.ArmJoint2 = msg.ArmJoint2
	r.state.ArmJoint3 = msg.ArmJoint3
	r.state.ArmJoint4 = msg.ArmJoint4
	r.stateChange <- r.state
}

func (r *Ros) JoyCallback(msg *sensor_msgs.Joy) {
	r.state.FrontFlippers = 0
	r.state.RearFlippers = 0

	if msg.Buttons[1] == 1 {

		Flippers = true
	}
	
	if msg.Buttons[2] == 1 {

		Flippers = false
	}
	
	if Flippers == true {
	
		if msg.Buttons[7] == 1 {
			r.state.RearFlippers = 0
			r.state.FrontFlippers = -0.1
		}
		
		if msg.Buttons[5] == 1 {
			r.state.RearFlippers = 0
			r.state.FrontFlippers = 0.1
		}
		
		if msg.Buttons[6] == 1 {
			r.state.FrontFlippers = 0
			r.state.RearFlippers = -0.1
		}

		if msg.Buttons[4] == 1 {
			r.state.FrontFlippers = 0
			r.state.RearFlippers = 0.1
		}
	}
	
	if math.Abs(float64(msg.Axes[1])) != 0.0 {
		if math.Abs(float64(msg.Axes[1])) < 0.15 {
			r.state.Linear = 0.000000000000001
		} else {
			r.state.Linear = float64(msg.Axes[1] / 2)
		}
	}
	
	if math.Abs(float64(msg.Axes[2])) != 0.0 {
		if math.Abs(float64(msg.Axes[2])) < 0.15 {
			r.state.Angular = 0.000000000000001
		} else {
			r.state.Angular = float64(msg.Axes[2] / 2)*(-1)
		}
	}
	
	fmt.Print("traseros: ")
	fmt.Print(r.state.RearFlippers)
	fmt.Print("\n")
	
	fmt.Print("delanteros: ")
	fmt.Print(r.state.FrontFlippers)
	fmt.Print("\n")

	
	r.stateChange <- r.state
}
