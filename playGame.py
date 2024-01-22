from minesweeperModule import *


def playGame():
    lp_path = "minesweeper.lp"
    url = "https://minesweeper.online/new-game"
    first_cell = "cell_4_4"

    # Connect to the website
    driver = webdriver.Chrome()
    driver.get(url)

    # Click the first cell
    click_id(driver, first_cell)

    # Read info from the site
    clingo_input, mx = get_clingo_input(driver, 9)

    # Write to clingo, solve given constraints + facts, filter output
    write_clingo_file(lp_path, clingo_input)
    left_clicks = filter_clingo_solve(lp_path, mx)

    # Run loop until solved
    solved = False

    while not solved:
        print(left_clicks)
        click_id(
            driver, left_clicks[0]
        )  # click on the first cell suggested by clingo solution
        clingo_input, mx = get_clingo_input(driver, 9)  # read info

        # Write to clingo, solve given constraints + facts, filter output
        write_clingo_file(lp_path, clingo_input)
        left_clicks = filter_clingo_solve(lp_path, mx)

        # Check if solved based on the "face" on the top

        face_class = driver.find_element(By.ID, "top_area_face").get_attribute("class")
        if face_class != "top-area-face zoomable hd_top-area-face-unpressed":
            solved = True
            time.sleep(30)


if __name__ == "__main__":
    playGame()
