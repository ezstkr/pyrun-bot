from browser import document as doc, window, timer, alert, aio
import javascript
Phaser = window.Phaser
import random


if(window.isChrome):
    from speech import recognition, utterance, synthesis


gameWidth = 560
gameHeight = 400

class Game(object):
    player = None
    cursors = None
    
    move_x = 0
    move_up = False

    speaking = False
    msg_panel = None
    msg = ""
    
    index = 0

    this = None

    is_open = False
    greeting = False
    def __init__(self):
        self.game = Phaser.Game.new(
            {
                'type': Phaser.AUTO,
                'parent': 'pydiv',
                'width': gameWidth,
                'height': gameHeight,
                'physics': {
                    'default': 'arcade',
                    'arcade': {
                        'gravity': {'y': 1000}
                    }
                },
                'scene': {
                    'preload': self.preload,
                    'create': self.create,
                    'update': self.update
                }
            }
        )
    def onresult(self, event, *args):
        current = event.resultIndex
        transcript = event.results[current][0].transcript

        self.speak(transcript)
        
        if(window.isChrome):
            def restart(*args):
                recognition.start()
            timer.set_timeout(restart, 1000)

        pass

    def onend(self, *args):
        pass
    
    def preload(self, *args):
        if(window.isChrome):
            recognition.onresult = self.onresult
            recognition.onend = self.onend

        self.this = javascript.this()
        this = javascript.this()
        this.load.image('sky', '../images/sky.png')
        this.load.image('ground', '../images/platform.png')
        this.load.image('star', '../images/star.png')
        this.load.image('bomb', '../images/bomb.png')
        this.load.spritesheet('bot', 
            '../images/bot2.png',
            { 'frameWidth': 120, 'frameHeight': 125 }
        )
        pass

    def create(self, *args):
        this = javascript.this()
        sky = this.add.image(280, 200, 'sky')
        sky.setScale(2)
        platforms = this.physics.add.staticGroup()
        platforms.create(280, 240, 'ground').setScale(0.4).refreshBody()
        platforms.create(280, 410, 'ground').setScale(2).refreshBody()


        self.player = this.physics.add.sprite(280, 125, 'bot')
        self.player.setBounce(0.2)
        self.player.setCollideWorldBounds(True)
        
        this.anims.create({
            'key': 'left',
            'frames': this.anims.generateFrameNumbers('bot', { 'start': 0, 'end': 1 }),
            'frameRate': 10,
            'repeat': -1
        })

        this.anims.create({
            'key': 'turn',
            'frames': [ { 'key': 'bot', 'frame': 2 } ],
            'frameRate': 20
        })

        this.anims.create({
            'key': 'right',
            'frames': this.anims.generateFrameNumbers('bot', { 'start': 3, 'end': 4 }),
            'frameRate': 10,
            'repeat': -1
        })

        this.physics.add.collider(self.player, platforms)

        self.msg_panel = self.this.add.text()
        self.msg_panel.setStyle({'fontSize': '14px', 'fill': '#ffffff' })

        self.user_panel = self.this.add.text()
        self.user_panel.setStyle({'fontSize': '14px', 'fill': '#ffffff' })
        self.user_panel.setPosition(500, 20)
        
        self.cursors = this.input.keyboard.createCursorKeys()
        this.input.keyboard.removeKey('space')
        pass

    def update(self, *args):
        this = javascript.this()
        try:
            self.index += 1
            self.index = self.index % 100
            if(self.index == 90 and self.is_open):
                self.predict()

            self.user_panel.setText(window.detected_name)
        except:
            pass
        

        if self.move_x != 0:
            if self.move_x > 0:
                self.move_x -= 1
                self.player.setVelocityX(self.move_x)
                self.player.anims.play('left', True)
            else:
                self.move_x += 1
                self.player.setVelocityX(self.move_x)
                self.player.anims.play('right', True)

        elif self.cursors.left.isDown:
            self.player.setVelocityX(-120)
            self.player.anims.play('left', True)
            
        elif self.cursors.right.isDown:
            self.player.setVelocityX(120)
            self.player.anims.play('right', True)
        else:
            self.player.setVelocityX(0)
            self.player.anims.play('turn')

        if (self.cursors.up.isDown and self.player.body.touching.down):
            self.player.setVelocityY(-560)

        if (self.move_up):
            self.player.setVelocityY(-560)
            self.move_up = False

        if (self.msg):
            self.msg_panel.setText(self.msg)
            self.msg_panel.setPosition(self.player.x + 24, self.player.y - 30)
        else:
            self.msg_panel.setText("")

                
        pass

    def left(self, x=120):
        self.move_x = -x

    def right(self, x=120):
        self.move_x = x
    
    def jump(self):
        self.move_up = True

    def speak(self, msg):
        self.msg = msg
        
        if(window.isChrome):
            utterance.text = msg
            synthesis.speak(utterance)

        def remove_msg():
            self.msg = ""
        timer.set_timeout(remove_msg, 1000)

        if "??????" in msg:
            self.left()
        if "??????" in msg:
            self.jump()
        if "?????????" in msg:
            self.right()

    def hello(self):
        msg = ""
        try:
            msg = f"??????, {window.detected_name}"
            self.speak(msg)
        except:
            msg = f"??????"
            self.speak(msg)
            pass
        
        

    def listen(self):
        if(window.isChrome):
            recognition.start()
        else:
            self.speak("?????? ????????????????????? ?????? ??? ?????????.")

    def stop_listen(self):
        if(window.isChrome):
            recognition.stop()
        else:
            self.speak("?????? ?????????????????????...")

    def learn(self, name):
        aio.run(learn(name))
        pass
    
    def predict(self):
        aio.run(predict())
        if(window.detected_name and not self.greeting):
            self.greeting = True
            self.speak(f"??????, {window.detected_name}")
        pass

    def eyes(self, is_open):
        aio.run(eyes(is_open))
        self.is_open = True



async def eyes(is_open):
    window.net = await window.mobilenet.load()
    window.camera = await window.tf.data.webcam(doc['webcam'])
    pass


async def learn(name):
    try:
        img = await window.camera.capture()
        activation = window.net.infer(img, True)
        window.classifier.addExample(activation, name)
        img.dispose()

        window.saveModel()
    except e:
        pass

async def predict():
    try:
        if (window.classifier.getNumClasses() > 0):
            img = await window.camera.capture()
            activation = window.net.infer(img, 'conv_preds')
            result = await window.classifier.predictClass(activation)
            window.detected_name = result.label
            img.dispose()
    except:
        pass


robot = Game()
