import turtle
import math

def draw_branch(t, length, angle_left, angle_right, depth, reduction_factor, max_depth):
    if depth == 0:
        return
    
    # Set color: coffee brown for the stem, green for branches
    if depth == max_depth:
        t.pencolor("#8B4513")  # stem color
    else:
        t.pencolor("green")  # Branch color
    
    # Set pen size: thicker for stem and larger branches, thinner for smaller ones
    pensize = max(1, depth * 2)  # Scale pen size with depth, minimum 1 pixel
    t.pensize(pensize)
    
    # Draw current branch
    t.forward(length)
    
    # Save current position and heading
    pos = t.position()
    heading = t.heading()
    
    # Draw left branch
    t.left(angle_left)
    draw_branch(t, length * reduction_factor, angle_left, angle_right, depth - 1, reduction_factor, max_depth)
    
    # Return to saved position and heading
    t.penup()
    t.setposition(pos)
    t.setheading(heading)
    t.pendown()
    
    # Draw right branch
    t.right(angle_right)
    draw_branch(t, length * reduction_factor, angle_left, angle_right, depth - 1, reduction_factor, max_depth)
    
    # Return to original position
    t.penup()
    t.setposition(pos)
    t.setheading(heading)
    t.pendown()

def main():
    # Get user inputs
    angle_left = float(input("Enter left branch angle (degrees): "))
    angle_right = float(input("Enter right branch angle (degrees): "))
    initial_length = float(input("Enter starting branch length (pixels): "))
    depth = int(input("Enter recursion depth: "))
    reduction_factor = float(input("Enter branch length reduction factor (e.g., 0.7 for 70%): "))
    
    # Setup turtle
    screen = turtle.Screen()
    t = turtle.Turtle()
    t.speed(0)  # Fastest drawing speed
    t.left(90)  # Start pointing up
    
    # Draw the tree, passing max_depth to track the initial depth
    draw_branch(t, initial_length, angle_left, angle_right, depth, reduction_factor, depth)
    
    # Keep window open until clicked
    screen.exitonclick()

if __name__ == "__main__":
    main()