from minesweeperModule import *


def playGame():
    lp_path = "minesweeper.lp"
    url = "https://minesweeper.online/new-game"
    first_cell = "cell_0_0"

    # Connect to the website
    driver = webdriver.Chrome()
    driver.get(url)

    time.sleep(10)
    # Click the first cell
    click_id(driver, first_cell)

    time.sleep(2)
    # Read info from the site
    clingo_input, mx = get_clingo_input(driver, 9)
    print(clingo_input)
    # Write to clingo, solve given constraints + facts, filter output
    # write_clingo_file(lp_path, clingo_input)
    left_clicks = filter_clingo_solve(lp_path, clingo_input, mx)

    # Run loop until solved
    solved = False

    while not solved:
        print(left_clicks[0])
        click_id(
            driver, left_clicks[0]
        )  # click on the first cell suggested by clingo solution
        time.sleep(2)
        clingo_input, mx = get_clingo_input(driver, 9)  # read info

        # Write to clingo, solve given constraints + facts, filter output
        # write_clingo_file(lp_path, clingo_input)
        left_clicks = filter_clingo_solve(lp_path, clingo_input, mx)

        # Check if solved based on the "face" on the top

        face_class = driver.find_element(By.ID, "top_area_face").get_attribute("class")
        if face_class != "top-area-face zoomable hd_top-area-face-unpressed":
            solved = True


if __name__ == "__main__":
    for i in range(10):
        try:
            playGame()
        except IndexError:
            playGame()
