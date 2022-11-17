from pathlib import Path
from src.atlas import sg
from maxconsole import get_theme, get_console
from maxprogress import get_progress
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from rich.prompt import IntPrompt, Confirm, PromptError
from time import sleep
from maxcolor import gradient, gradient_panel


console = get_console(get_theme())
progress = get_progress(console)

DRIVER_PATH = Path.cwd() / "driver" / "chromedriver"


def download_chapter(chapter: int) -> str:
    """
    Download the text of a chapter from the Super Gene website.

    Args:
        `chapter` (int): The chapter number.

    Returns:
        `unparsed_text` (str): The text of the chapter.
    """
    # Initial Variables
    chapter_str = str(chapter)

    lines = []
    title_prefix = "Super Gene Chapter "
    title_suffix = " Online | BestLightNovel.com"

    # Get URL
    sg()
    doc = Chapter.objects(chapter=chapter).first()  # type: ignore
    URL = doc.url

    # Chrome Webdriver
    PATH = str(DRIVER_PATH)
    options = ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(PATH, options=options)

    with progress:
        download_chapter_text = progress.add_task(
            description=f"Downloading text for Chapter {chapter}...", total=3
        )
        # Get Chapter Page
        driver.get(URL)

        # Get article title
        article_title = driver.title
        article_title = str(article_title)
        article_title = article_title.replace(title_prefix, "").replace(
            title_suffix, ""
        )
        progress.advance(download_chapter_text)

        try:
            settings_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.LINK_TEXT, "SETTING"))
            )
            settings_button.click()

            change_bad_words_button = driver.find_element(
                By.XPATH, '//*[@id="trang_doc"]/div[6]/div[1]/div[2]/ul/li[5]/a'
            )
            change_bad_words_button.click()
            try:
                text = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "vung_doc"))
                )
                text = driver.find_element(By.ID, "vung_doc")
                paragraphs = text.find_elements(By.TAG_NAME, "p")
                text = ""
                progress.update(
                    task_id=download_chapter_text,
                    advance=1,
                    description="Downloaded chapter. Parsing text...",
                )
                for x, paragraph in enumerate(paragraphs):
                    if x == 0 | x == 1:
                        chapter_title = f"Chapter {chapter}"
                        if chapter_title in paragraph:
                            continue
                        else:
                            text = str(f"{text}{paragraph.text}\n\n")

                # Strip erroneous whitespace characters
                progress.update(
                    task_id=download_chapter_text,
                    advance=1,
                    description="Trimmed chapter text. Stripping erroneous whitespace...",
                )
                text = text.strip()

                # Save text to MongoDB
                doc.text = text
                doc.save()

            except:
                print(
                    "\n\n\nError 404\nUnable to locate text on page. Quitting Script.\n"
                )
        finally:
            driver.quit()
        return doc.text


if __name__ == "__main__":

    chapter = IntPrompt.ask(
        gradient("Enter the chapter number you wish to re-download"), console=console
    )
    if not isinstance(chapter, int):
        raise PromptError(f"{chapter} is not a valid integer.")
    elif chapter > 3462:
        raise PromptError(f"Chapter {chapter} is not a valid chapter number.")
    elif chapter == 3095 | chapter == 3117:
        raise ValueError(f"Chapter {chapter} is not a valid chapter number.")
    elif chapter <= 0:
        raise ValueError(f"Chapter {chapter} is not a valid chapter number.")
    else:
        chapter_str = str(chapter)

    overwrite = Confirm.ask(
        gradient(
            f"Would you like to overwrite chapter {chapter_str}'s current text in MongoDB?"
        ),
        console=console,
        default="n",
        show_default=True,
    )
    match overwrite:
        case "n" | "N" | "no" | "No":
            overwrite = "n"
        case "y" | "Y" | "yes" | "Yes":
            overwrite = "y"
        case _:
            raise PromptError("Response was not valid. Response: {overwrite}")
    console.print(gradient_panel(f"Downloading Chapter {chapter}..."))
    unparsed_text = download_chapter(chapter)

    # Write Unparsed Text to Disk
    sg()
