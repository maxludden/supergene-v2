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
from rich.panel import Panel
from time import sleep
from maxcolor import gradient, gradient_panel


console = get_console(get_theme())
progress = get_progress(console)

DRIVER_PATH = Path.cwd() / "driver" / "chromedriver"


def download_chapter(chapter: int) -> dict[str:int|str]:
    """Download the text of a chapter from the Super Gene website.

    Args:
        chapter (`int`): The chapter number.

    Returns:
        chapter_data (`dict[str:int|str]`):
            chapter (`int`): The downloaded chapter's number.
            title (`str`): The title of the downloaded chapter.
            text (`str`): The text of the downloaded chapter.
    """

    # Initial Variables
    chapter_str = str(chapter)
    lines = []
    title_prefix = "Super Gene Chapter "
    title_suffix = " Online | BestLightNovel.com"

    # Get URL
    sg() # Access MongoDB
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

            except:
                print(
                    "\n\n\nError 404\nUnable to locate text on page. Quitting Script.\n"
                )
                raise RuntimeError(f"Unable to locate text on webpage: `{URL}`")
        finally:
            driver.quit()

        chapter_data = {
            "chapter": chapter,
            "title": article_title,
            "text": text
        }
        return chapter_data


def chapter_prompt() -> int:
    """Prompt the user to enter the chapter number they would like to re-download.
    Returns:
        chapter (`int`): The chapter number to re-download.

    Raises:
        `PromptError`: If the prompt returns a value that is not an integer.
        `PromptError`: If the prompt returns a value greater than `3462` as there are only `3462` chapters.
        `ValueError`: If the prompt returns either of the skipped chapters (`Chapter 3095` or `Chapter 3117`).
        `ValueError`: If the prompt returns `0` as the first chapter is `Chapter 1`.
    """
    chapter_input = IntPrompt.ask(
        gradient("Enter the chapter number you wish to re-download"), console=console
    )
    if not isinstance(chapter_input, int):
        raise PromptError(f"{chapter_input} is not a valid integer.")
    elif chapter_input > 3462:
        raise PromptError(f"Chapter {chapter_input} is not a valid chapter number.")
    elif chapter_input == 3095 | chapter_input == 3117:
        raise ValueError(f"Chapter {chapter_input} is not a valid chapter number.")
    elif chapter_input <= 0:
        raise ValueError(f"Chapter {chapter_input} is not a valid chapter number.")
    else:
        chapter = chapter_input
    return chapter


def overwrite_prompt(chapter: int) -> bool:
    """Generates a prompt whether to overwrite the existing chapters text in MongoDB.

    Args:
        chapter (`int`): The chapter number that could be overwrite.

    Raises:
        PromptError: If the prompt returns a non-boolean value.

    Returns:
        bool: Whether to overwrite the existing chapter's text in MongoDB.
    """
    overwrite = Confirm.ask(
        gradient(
            f"Would you like to overwrite chapter {chapter}'s current text in MongoDB?"
        ),
        console=console,
        default="n",
        show_default=True,
    )
    match overwrite:
        case "n" | "N" | "no" | "No":
            overwrite = False
        case "y" | "Y" | "yes" | "Yes":
            overwrite = True
        case _:
            raise PromptError("Response was not valid. Response: {overwrite}")
    return overwrite


def display_chapter(chapter_data: dict[str:int|str]) -> None:
    """Display the downloaded chapter to the console.

    Args:
        chapter_data (`dict[str:int|str]`)
    """

if __name__ == "__main__":
    chapter = chapter_prompt()
    chapter_data = download_chapter(chapter)

    overwrite = input["overwrite"]
    console.print(gradient_panel(f"Downloading Chapter {chapter}..."))
    unparsed_text = download_chapter(chapter)

    # Write Unparsed Text to Disk
    sg()
