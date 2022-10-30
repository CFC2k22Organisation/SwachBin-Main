#Code written for IBM Call for code 2K22 (SwachBin)
import cv2
from time import sleep
import os
import warnings
import torch
import torchvision
from torch.utils.data import random_split
import torchvision.models as models
import torch.nn as nn 
import torch.nn.functional as F
from torchvision.datasets import ImageFolder
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
from PIL import Image
from pathlib import Path
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
from playsound import playsound
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import time
warnings.filterwarnings("ignore")

###################################
#GPIO setup for servo
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(17, GPIO.OUT)
#GPIO setup for LED
#GPIO.setup(27,GPIO.OUT) #13 - cd
#GPIO.setup(5,GPIO.OUT) #29 -dry
#GPIO.setup(12,GPIO.OUT) #32 -Hazardous
#GPIO.setup(26,GPIO.OUT) #37 -sanitary
#GPIO.setup(24,GPIO.OUT) #18 -wet
#GPIO.setup(23,GPIO.OUT) #16 -mixed

########################################################
#to capture photo from raspberrypi camera

videoCaptureObject = cv2.VideoCapture(0)
result = True
count=1
fps = int(videoCaptureObject.get(cv2.CAP_PROP_FPS))
while(result):
    
    ret,frame = videoCaptureObject.read()
    if count%(3*fps) == 0 :
        cv2.imwrite("image.jpg",frame)
        result = False

    count+=1
#print(count)
print("captured photo- SUCCESS")
videoCaptureObject.release()



#########################################################
#main code to pass image and model to predict class
data_dir  = '/home/pi/CFC/model2/data'
classes = os.listdir(data_dir) 
transformations = transforms.Compose([transforms.Resize((256, 256)), transforms.ToTensor()])
dataset = ImageFolder(data_dir, transform = transformations)


def show_sample(img, label):
    print("Label:", dataset.classes[label], "(Class No: "+ str(label) + ")")
    plt.imshow(img.permute(1, 2, 0))

def get_default_device():
    """Pick GPU if available, else CPU"""
    if torch.cuda.is_available():
        return torch.device('cuda')
    else:
        return torch.device('cpu')
    
def to_device(data, device):
    """Move tensor(s) to chosen device"""
    if isinstance(data, (list,tuple)):
        return [to_device(x, device) for x in data]
    return data.to(device, non_blocking=True)

def accuracy(outputs, labels):
    _, preds = torch.max(outputs, dim=1)
    return torch.tensor(torch.sum(preds == labels).item() / len(preds))

class DeviceDataLoader():
    """Wrap a dataloader to move data to a device"""
    def __init__(self, dl, device):
        self.dl = dl
        self.device = device
        
    def __iter__(self):
        """Yield a batch of data after moving it to device"""
        for b in self.dl: 
            yield to_device(b, self.device)

    def __len__(self):
        """Number of batches"""
        return len(self.dl)

class ImageClassificationBase(nn.Module):
    def training_step(self, batch):
        images, labels = batch 
        out = self(images)                  # Generate predictions
        loss = F.cross_entropy(out, labels) # Calculate loss
        return loss
    
    def validation_step(self, batch):
        images, labels = batch 
        out = self(images)                    # Generate predictions
        loss = F.cross_entropy(out, labels)   # Calculate loss
        acc = accuracy(out, labels)

class ResNet(ImageClassificationBase):
    def __init__(self):
        super().__init__()
        # Use a pretrained model
        self.network = models.resnet50(pretrained=True)
        # Replace last layer
        num_ftrs = self.network.fc.in_features
        self.network.fc = nn.Linear(num_ftrs, len(dataset.classes))
    
    def forward(self, xb):
        return torch.sigmoid(self.network(xb))


model = ResNet()

model = torch.load('/home/pi/CFC/model2/my_model.pt')

device = get_default_device()

def predict_image(img, model):
    # Convert to a batch of 1
    xb = to_device(img.unsqueeze(0), device)
    # Get predictions from model 
    yb = model(xb)
    # Pick index with highest probability
    prob, preds  = torch.max(yb, dim=1)
    # Retrieve the class label
    return dataset.classes[preds[0].item()]

def predict_external_image(image_name):
    image = Image.open(Path('./' + image_name))
    example_image = transformations(image)
    plt.imshow(example_image.permute(1, 2, 0))
    #print("The image resembles", predict_image(example_image, model) + ".")
    return predict_image(example_image, model)

#Actual prediction of image class
pred_class = predict_external_image('image.jpg')

cat=""
#Classifying image into Recyclable/Non-Recyclable and trigger servo motor
if pred_class=="dry" or pred_class=="wet":
    cat= "Recyclable"
    print(cat)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT)
    pwm=GPIO.PWM(18, 50)
    pwm.start(0)
    pwm.ChangeDutyCycle(5) 
    sleep(4)
    pwm.ChangeDutyCycle(10) 
    sleep(1)
    pwm.stop()
    GPIO.cleanup()
else:
    #print("category= Non-recyclable")
    cat= "Non-Recyclable"
    print(cat)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT)
    pwm=GPIO.PWM(18, 50)
    pwm.start(0)
    pwm.ChangeDutyCycle(12.5) 
    sleep(4)
    pwm.ChangeDutyCycle(10) 
    sleep(1)
    pwm.stop()
    GPIO.cleanup()

#Turning LED on to indicate the class
if pred_class=="dry":
    PIO.setmode(GPIO.BCM)
    GPIO.setup(27,GPIO.OUT)
    GPIO.output(27,GPIO.HIGH)
    sleep(5)
    GPIO.output(27,GPIO.LOW)
elif pred_class=="cd":
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(5,GPIO.OUT)
    GPIO.output(5,GPIO.HIGH)
    sleep(5)
    GPIO.output(12,GPIO.LOW)
elif pred_class=="Hazardous":
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(23,GPIO.OUT)
    GPIO.output(23,GPIO.HIGH)
    sleep(5)
    GPIO.output(23,GPIO.LOW)
elif pred_class=="wet":
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(24,GPIO.OUT)
    GPIO.output(24,GPIO.HIGH)
    sleep(5)
    GPIO.output(24,GPIO.LOW)
elif pred_class=="sanitary":
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(12,GPIO.OUT)
    GPIO.output(12,GPIO.HIGH)
    sleep(5)
    GPIO.output(12,GPIO.LOW)
else:
    #mixed waste
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(23,GPIO.OUT)
    GPIO.output(23,GPIO.HIGH)
    sleep(5)
    GPIO.output(23,GPIO.LOW)
    
#Speaker to greet the user
authenticator = IAMAuthenticator('w9BnLVJn7bNkplaRmatr8qps1RxMbozXN1N68KuS-Pcz')
text_to_speech = TextToSpeechV1(authenticator=authenticator)
text_to_speech.set_service_url('https://api.au-syd.text-to-speech.watson.cloud.ibm.com/instances/45faaf38-33db-49b9-85a2-37a1a6cac7ae')

var="Thank you for using Swach Bin. "+"The waste type is  "+pred_class + ". It is "+cat

with open('Voice.wav', 'wb') as audio_file:
    audio_file.write(text_to_speech.synthesize(var,voice='en-US_AllisonV3Voice',accept='audio/wav').get_result().content)

playsound('/home/pi/CFC/model2/Voice.wav',block=False)
print('playing Voice using speaker')

#Ultrasonic sensor to measure the waste deposit level in the bin

#Configuring to IBM IoT platform
ORG = "lw59h1"
DEVICE_TYPE = "SwachBin"
TOKEN = ")whpKZC4BqD8b2c&l2"
DEVICE_ID = "e45f0142fbe8"
server = ORG + ".messaging.internetofthings.ibmcloud.com";
pubTopic1 = "iot-2/evt/Waste level/fmt/json";
authMethod = "use-token-auth";
token = TOKEN;
clientId = "d:" + ORG + ":" + DEVICE_TYPE + ":" + DEVICE_ID;

#Initial GPIO setup
TRIG = 21
ECHO = 20
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.output(TRIG, False)
print("Calibrating.....")
sleep(2)
mqttc = mqtt.Client(client_id=clientId)
mqttc.username_pw_set(authMethod, token)
mqttc.connect(server, 1883, 60)
GPIO.output(TRIG, True)
sleep(0.00001)
GPIO.output(TRIG, False)
 
while GPIO.input(ECHO)==0:
    pulse_start = time.time()
 
while GPIO.input(ECHO)==1:
    pulse_end = time.time()
 
pulse_duration = pulse_end - pulse_start 
distance = pulse_duration * 17150
distance = round(distance+1.15, 2)      
mqttc.publish(pubTopic1, distance)
if distance<=3:
    print("The SwachBin is Full")
print("Waste-level data uploaded to IBM")

 
