import pygame
import pygame_gui

from cell import Cell

# Constants
ROWS = 10
COLS = 20
CELL_SIZE = 30
CELL_BORDER = 1
BORDER_COLOR = pygame.Color(127, 127, 127)
BOTTOM_HEIGHT = 150
WINDOW_SIZE = (COLS*CELL_SIZE, ROWS*CELL_SIZE+BOTTOM_HEIGHT)

# Cells creation
temp_grid = []
cells = []
for row in range(ROWS):
    temp_grid.append([])
    for col in range(COLS):
        cell = Cell(row, col, CELL_SIZE, CELL_BORDER)
        temp_grid[row].append(cell)
        cells.append(cell)

# Cells organisation
# TODO: upgrade neighboring system
for row in range(ROWS):
    for col in range(COLS):
        cell = temp_grid[row][col]
        cell.neighbors += [temp_grid[(row-1)%ROWS][(col-1)%COLS],
                           temp_grid[(row-1)%ROWS][ col   %COLS],
                           temp_grid[(row-1)%ROWS][(col+1)%COLS],
                           temp_grid[ row   %ROWS][(col-1)%COLS],
                           temp_grid[ row   %ROWS][(col+1)%COLS],
                           temp_grid[(row+1)%ROWS][(col-1)%COLS],
                           temp_grid[(row+1)%ROWS][ col   %COLS],
                           temp_grid[(row+1)%ROWS][(col+1)%COLS]]
del temp_grid

pygame.init()
pygame.display.set_caption("Conway's Game of Life")
window = pygame.display.set_mode(WINDOW_SIZE)
window.fill(BORDER_COLOR)
clock = pygame.time.Clock()

# User Interface
gui = pygame_gui.UIManager(WINDOW_SIZE)
play_btn = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((5, WINDOW_SIZE[1]-BOTTOM_HEIGHT + 5),
    (100, 50)), text='Play', manager=gui
)
pause_btn = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((5, WINDOW_SIZE[1]-BOTTOM_HEIGHT + 60),
    (100, 50)), text='Pause', manager=gui
)

run = True
pause = False
while run:

    dt = clock.tick(60)         # ms
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            pause = not pause

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            if event.pos[1] < ROWS*CELL_SIZE:
                cell = cells[COLS*(event.pos[1]//CELL_SIZE) + event.pos[0]//CELL_SIZE]
                cell.set_state(not cell.is_alive())
        
        elif event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == play_btn:
                pause = False
            elif event.ui_element == pause_btn:
                pause = True
            

        gui.process_events(event)
    
    gui.update(dt)

    for cell in cells:
        cell.draw(window)

    if not pause:    
        for cell, new_state in [(cell, cell.get_next_state()) for cell in cells]:
            cell.set_state(new_state)

    gui.draw_ui(window)
    pygame.display.update()

pygame.quit()