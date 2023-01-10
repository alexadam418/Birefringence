import clr
import time

clr.AddReference("C:\Program Files\Thorlabs\Kinesis\Thorlabs.MotionControl.DeviceManagerCLI.dll")
clr.AddReference("C:\Program Files\Thorlabs\Kinesis\Thorlabs.MotionControl.GenericMotorCLI.dll")
clr.AddReference("C:\Program Files\Thorlabs\Kinesis\ThorLabs.MotionControl.KCube.DCServoCLI.dll")

from Thorlabs.MotionControl.DeviceManagerCLI import *
from Thorlabs.MotionControl.GenericMotorCLI import *
from Thorlabs.MotionControl.GenericMotorCLI import KCubeMotor
from Thorlabs.MotionControl.GenericMotorCLI.ControlParameters import JogParametersBase
from Thorlabs.MotionControl.KCube.DCServoCLI import *
from System import Decimal


def homepolariser():
    serial_num = str('27263222')
    DeviceManagerCLI.BuildDeviceList()
    controller = KCubeDCServo.CreateKCubeDCServo(serial_num)
    if not controller == None:
        controller.Connect(serial_num)
        if not controller.IsSettingsInitialized():
            controller.WaitForSettingsInitialized(3000)
        controller.StartPolling(50)
        time.sleep(.1)
        controller.EnableDevice()
        time.sleep(.1)

        config = controller.LoadMotorConfiguration(serial_num,
                                                   DeviceConfiguration.DeviceSettingsUseOptionType.UseFileSettings)
        config.DeviceSettingsName = str('PRM1-Z8')
        config.UpdateCurrentConfiguration()
        controller.SetSettings(controller.MotorDeviceSettings, True, False)
        controller.Home(60000)
        controller.StopPolling()
        controller.Disconnect(False)



def movepolariser(ang):
    serial_num = str('27263222')
    DeviceManagerCLI.BuildDeviceList()
    controller = KCubeDCServo.CreateKCubeDCServo(serial_num)
    print("hello")
    if not controller == None:
        controller.Connect(serial_num)
        if not controller.IsSettingsInitialized():
            controller.WaitForSettingsInitialized(3000)
        controller.StartPolling(50)
        time.sleep(.1)
        controller.EnableDevice()
        time.sleep(.1)

        config = controller.LoadMotorConfiguration(serial_num,
                                                   DeviceConfiguration.DeviceSettingsUseOptionType.UseFileSettings)
        config.DeviceSettingsName = str('PRM1-Z8')
        config.UpdateCurrentConfiguration()
        controller.SetSettings(controller.MotorDeviceSettings, True, False)
        #print('Homing Motor')
        #controller.Home(60000)
        jog_params = controller.GetJogParams()
        jog_params.StepSize = Decimal(10)
        jog_params.MaxVelocity = Decimal(10)
        jog_params.JogMode = JogParametersBase.JogModes.SingleStep

        controller.SetJogParams(jog_params)
        print("Moving Motor")
        #controller.MoveJog(MotorDirection.Forward, 60000)
        controller.MoveTo(Decimal(ang), 60000)
        controller.StopPolling()
        controller.Disconnect(False)
