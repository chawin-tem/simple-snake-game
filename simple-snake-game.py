from graphics import Canvas
import time
import random
    
CANVAS_WIDTH = 400
CANVAS_HEIGHT = 400
SIZE = 20

# if you make this larger, the game will go slower
DELAY = 0.1

def main():
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    left_x = 0
    top_y = left_x
    right_x = left_x + SIZE
    bottom_y = top_y + SIZE
    # for accelerating the game
    new_delay = DELAY
    # points
    points = 0
    # list of snake's coordinates
    snake_history = []
    last_pos_x = 0
    last_pos_y = 0
    snake_tail_status = False
    snake_tail = []
    snake_index = 0
    # direction history
    dir_his = ['right']
    
    start_game(canvas)
    
    # draw the food
    food = draw_food(canvas)
    # draw the snake
    snake_head = canvas.create_rectangle(left_x, top_y, right_x, bottom_y, "green")
    canvas.set_outline_color(snake_head, 'black')
    # initialize point
    point_text = canvas.create_text(10, 375, font_size=20, text=str(points)+' points', color='grey')
    
    # direction variables
    # initial setting is going right
    snake_dir_x = 20
    snake_dir_y = 0

    while True:
        # sleep first to show the snake's starting position frame
        time.sleep(new_delay)
        
        # keys handling
        key = canvas.get_last_key_press()
        # print(key)
        if key == 'ArrowLeft' and dir_his[0] != 'right':
            snake_dir_x = -20
            snake_dir_y = 0
            dir_his.insert(0, 'left')
            dir_his.pop()

        elif key == 'ArrowRight' and dir_his[0] != 'left':
            snake_dir_x = 20
            snake_dir_y = 0
            dir_his.insert(0, 'right')
            dir_his.pop()

        elif key == 'ArrowUp' and dir_his[0] != 'down':
            snake_dir_x = 0
            snake_dir_y = -20
            dir_his.insert(0, 'down')
            dir_his.pop()

        elif key == 'ArrowDown' and dir_his[0] != 'up':
            snake_dir_x = 0
            snake_dir_y = 20
            dir_his.insert(0, 'up')
            dir_his.pop()
            
        canvas.move(snake_head, snake_dir_x, snake_dir_y)
        # move snake tail with for loop
        for i in range(len(snake_tail)):
            canvas.moveto(snake_tail[i], snake_history[i][0], snake_history[i][1])
            
        # keep up with snake_head's coordinates
        snake_coor_x = canvas.get_left_x(snake_head)
        snake_coor_y = canvas.get_top_y(snake_head)
        
        # check collide with self with for loop
        if snake_eat_self(canvas, snake_coor_x, snake_coor_y, snake_tail) == True:
            break
        
        # get coordinate of last grid
        snake_history.insert(0,[snake_coor_x, snake_coor_y])
        if len(snake_history) > 400:
            snake_history.pop()
            
        if len(snake_history) > 1:
            last_pos_x = snake_history[snake_index][0]
            last_pos_y = snake_history[snake_index][1]
        
        # set the border
        if check_collision(canvas, snake_coor_x, snake_coor_y) == True:
            break
        
        # snake_head eat food
        if snake_eat_food(canvas, snake_coor_x, snake_coor_y) == True:
            # accelerator
            new_delay = new_delay * 0.9
            # increase point
            points += 1
            canvas.delete(point_text)
            point_text = canvas.create_text(10, 375, font_size=20, text=str(points)+' points', color='grey')
            # move food to random position
            canvas.moveto(food, random.randrange(0, CANVAS_WIDTH - SIZE, 20), random.randrange(0, CANVAS_WIDTH - SIZE, 20))
            # to draw snake tail
            # draw snake tail at snake_history index 1
            snake_tail_status = True
            color = ['coral', 'linen', 'moccasin', 'lightblue', 'burlywood', 'orchid', 'fuchsia', 'gainsboro', 'honeydew', 'ivory']
            random_color = random.choice(color)
            snake_tail.append(canvas.create_rectangle(last_pos_x, last_pos_y, last_pos_x + SIZE, last_pos_y + SIZE, color = random_color))
            snake_index += 1
            # move to the latest grid

    # Game over if snake crash the border
    canvas.create_text(55, 180, font_size=50, text='GAME OVER', color='red')
    
def start_game(canvas):
    start_text = canvas.create_text(70, 180, font_size=50, text='click to start', color='green')
    canvas.wait_for_click()
    canvas.delete(start_text)

def draw_food(canvas):
    max_value = CANVAS_WIDTH - SIZE
    t_left_x = random.randrange(0, max_value, 20)
    t_top_y = random.randrange(0, max_value, 20)
    t_right_x = t_left_x + SIZE
    t_bottom_y = t_top_y + SIZE
    
    target = canvas.create_oval(t_left_x, t_top_y, t_right_x, t_bottom_y, "salmon")
    return target
    
def check_collision(canvas, snake_coor_x, snake_coor_y):
    if snake_coor_x >= 400:
        snake_head = canvas.create_rectangle(snake_coor_x - SIZE, snake_coor_y, snake_coor_x, snake_coor_y + SIZE, "green")
        return True
    if snake_coor_x < 0:
        snake_head = canvas.create_rectangle(0, snake_coor_y, SIZE, snake_coor_y + SIZE, "green")
        return True
    if snake_coor_y >= 400:
        snake_head = canvas.create_rectangle(snake_coor_x, snake_coor_y - SIZE, snake_coor_x + SIZE, snake_coor_y, "green")
        return True
    if snake_coor_y < 0:
        snake_head = canvas.create_rectangle(snake_coor_x, 0, snake_coor_x + SIZE, SIZE, "green")
        return True
    return False
    
def snake_eat_food(canvas, snake_coor_x, snake_coor_y):
    snake_eat = canvas.find_overlapping(snake_coor_x, snake_coor_y, snake_coor_x + SIZE, snake_coor_y + SIZE)
    if 'shape_1' in snake_eat:
        return True
    return False
    
def snake_eat_self(canvas, snake_coor_x, snake_coor_y, snake_tail):
    snake_eat = canvas.find_overlapping(snake_coor_x, snake_coor_y, snake_coor_x + SIZE, snake_coor_y + SIZE)
    for shape in snake_tail:
        if shape in snake_eat:
            return True
    return False
    
if __name__ == '__main__':
    main()