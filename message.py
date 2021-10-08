import time, requests, json
import base64
import Key


class Message:
    k = Key.Key()
    kA = k.get_key()

    from_no = ""  #wirte your phone number
    to_no = None
    name = None
    location = None
    message = None
    data = None

    def __init__(self, to_no, name, location):
        self.set_basic(to_no, name, location)
        self.set_message()
        self.set_data()

    def set_basic(self, to_no, name, location):
        self.to_no = to_no
        self.name = name
        self.location = location

    def set_message(self):
        self.message = self.name + "님의 낙상사고가 발생했습니다. " + self.location

    def set_data(self):
        self.data = {
            'type': '',
            'countryCode': '82',
            'from': "{}".format(self.from_no),
            'contentType': 'COMM',
            'content': "{}".format(self.message),
            'messages': [{'to': "{}".format(self.to_no)}]
        }

    def get_data(self):
        return self.data

    def send(self):
        response = requests.post(
            self.kA[0], data=json.dumps(self.data),
            headers={"Content-Type": "application/json; charset=utf-8",
                     "x-ncp-apigw-timestamp": str(self.kA[1]),
                     "x-ncp-iam-access-key": self.kA[2],
                     "x-ncp-apigw-signature-v2": self.kA[3]}
        )
        print(response.text)


class SMS(Message):
    def __int__(self, to_no, name, location):
        super().set_basic(to_no, name, location)
        super().set_message()
        self.set_data()

    def set_data(self):
        super().set_data()
        self.data['type'] = 'SMS'


class MMS(Message):
    time = None
    image = {"name": "", "body": ""}

    def __init__(self, to_no, name, location, image_name):
        super().set_basic(to_no, name, location)
        self.set_time()
        self.set_message()
        self.set_image(image_name)
        self.set_data()

    def set_time(self):
        now = time.localtime(time.time())
        self.time = time.strftime('[%H시%M분] ', now)

    # image_name은 jpg 또는 jpeg 확장자만 가능
    def set_image(self, image_name):
        self.image['name'] = image_name
        with open(image_name, 'rb') as img:
            self.image['body'] = base64.b64encode(img.read()).decode('utf-8')

    def set_message(self):
        self.message = self.time + self.name + "님의 낙상사고가 발생했습니다. " + self.location

    def set_data(self):
        super().set_data()
        self.data['type'] = 'MMS'
        self.data['subject'] = '낙상알림'
        self.data['files'] = [{"name": self.image['name'], "body": "{}".format(self.image['body'])}]

