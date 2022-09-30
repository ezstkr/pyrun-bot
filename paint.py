from browser import document
import turtle

def init(_type=""):
    turtle.restart()
    turtle.set_defaults(
        canvwidth = 800,  # default is 500
        canvheight = 500,  # default is 500
        turtle_canvas_wrapper = document['turtle-div']
    )
    if _type is "turtle":
        return turtle.Turtle("turtle")
    else:
        return turtle.Turtle()

def done():
    turtle.done()
    