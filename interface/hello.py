from camera import pyspin_cam as pc
import PySpin as spin
#from camera.pyspin_cam import Camera

print('1')
cam = pc.Camera()




print('2')
print(cam['Gain'].value)
cam['StreamBufferHandlingMode'].value = 'NewestOnly'
print(cam['StreamBufferHandlingMode'].value)
cam['TriggerMode'].value = 'Off'
print(cam['TriggerMode'].value)
#        acquisition_frame_rate_enable = self.camera.AcquisitionFrameRateEnable
#        acquisition_frame_rate_enable.SetValue(True)
#        self.camera.AcquisitionFrameRate.SetValue(self.camera.AcquisitionFrameRate.GetMax())

print(cam['StreamBufferCountMode'].value)


cam['StreamBufferCountMode'].value.rsplit('_',1)[1]

print(cam['StreamBufferCount'+cam['StreamBufferCountMode'].value.rsplit('_',1)[1]].value)

cam['StreamBufferCountMode'].value = 'Manual'
print(cam['StreamBufferCountManual'].value)
#cam.Init()
cam.BeginAcquisition()
print('acquisition')
cam.EndAcquisition()
print('ended')
cam.DeInit()
cam.Clear_cam_list()
cam.Delete()
cam.ReleaseInstance()
print('released')
del cam

cam2 = pc.Camera()
print(cam2['StreamBufferCountMode'].value)
cam2.BeginAcquisition()
cam2.EndAcquisition()
print('ended')
cam2.DeInit()
cam2.Clear_cam_list()
cam2.Delete()
cam2.ReleaseInstance()
del cam2

#
#print(cam['BlackLevelAuto'].value)
#print(cam['BlackLevelAutoBalance'].value)
#print(cam['BalanceWhiteAuto'].value)
#print(cam['GainAutoTapBalanceand'].value)
#print(cam['BlackLevelAutoTapBalance'].value)

#cam.release()
