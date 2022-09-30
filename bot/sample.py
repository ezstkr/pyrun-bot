from ai import robot
from random import choice

robot.eyes(True)

def listening(message):
    
    if "안녕" in message:
        response = ['반갑다', '안뇽', '방가방가']
        robot.speak( choice( response ))

    elif "조용" in message:
        robot.listen(False)
    
    elif "바보" in message:
        robot.speak('ㅠㅠ')
        robot.jump()
    
    elif "이름" in message:
        robot.speak( f"저의 이름은 {robot.name} 입니다." )
        

def detected(name):
    if "졸음" in name:
        robot.speak(f"졸지마세요." )
    
    elif "엄마" in name:
        robot.speak(f"앗! 엄마가 지켜보고 있습니다. 조심!" )
    
    elif "좌" in name:
        robot.left()
        
    elif "우" in name:
        robot.right()