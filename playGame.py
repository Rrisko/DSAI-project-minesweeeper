from minesweeperModule import *

lp_path = "minesweeper.lp"
url = "https://minesweeper.online/new-game"
driver = webdriver.Chrome()
driver.get(url)

click_id(driver, "cell_4_4")

clingo_input, mx = get_clingo_input(driver, 9)

write_clingo_file(lp_path, clingo_input)

left_clicks = filter_clingo_solve(lp_path, mx)

solved = False


while not solved:
    click_id(driver, left_clicks[0])

    clingo_input, mx = get_clingo_input(driver, 9)

    write_clingo_file(lp_path, clingo_input)

    left_clicks = filter_clingo_solve(lp_path, mx)

    face_class = driver.find_element(By.ID, "top_area_face").get_attribute("class")
    if face_class == "top-area-face zoomable hd_top-area-face-unpressed":
        solved = False
    else:
        solved = True
        time.sleep(30)
