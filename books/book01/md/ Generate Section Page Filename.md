def generate_section_files(
    section: int, save: bool = True, filepath: bool = True
) -> List[str] | List[Path]: # type: ignore
    """
    Generates a list of filenames/filepaths of a given section's Section Page followed by it's chapters.

​    Args:
​        `section` (int): The given section.

​        `filepath` (bool): Whether to generate the the full filepath for the files. Defaults to is False.

​    Returns:
​        `section_files` (list[str] | list[Path]): The ordered contents of the given section.

​    """
​    files = []
​    sg()
​    doc = sec.Section.objects(section=section).first()  # type: ignore
​    with Progress(console=console) as progress:
​        if not filepath:
​            filepaths_task = progress.add_task(
​                "Generating Section Files' Filenames...", total=len(doc.chapters) + 1
​            )

​            part = doc.part

            # > Generate Section Page Filename
​            section_page_filename = f"{doc.filename}.html"
​            files.append(section_page_filename)
​            progress.update(filepaths_task, advance=1)  # Update Progress Bar

            # > Generate Chapter Filenames
​            chapter_count = 0
​            for chapter in doc.chapters:
​                chapter_filename = f"chapter-{str(chapter).zfill(4)}.html"
​                files.append(chapter_filename)
​                chapter_count += 1

                # Update Progress Bar
​                progress.update(filepaths_task, advance=1)

​            console.print(
​                default_panel(section, "Section Files", files, 579), highlight=True
​            )
​            sg()
​            if save:
​                section_doc = sec.Section.objects(section=section) # type: ignore
​                if sec.Section.objects

​        else:
​            filenames_task = progress.add_task(
​                "Generating Section Filepaths...", total=len(doc.chapters) + 1
​            )

            # > Access Section Doc from MongoDb
​            section_doc = sec.Section.objects(section=section).first()  # type: ignore
​            section_part = section_doc.part

            # > Generate Section Page Filepath
​            section_page_filepath = section_doc.html_path
​            files.append(section_page_filepath)
​            progress.update(filenames_task, advance=1)  # Update Progress Bar

            # > Generate Chapter Filepaths
​            for doc in section_doc.chapters:
​                chapter_doc = ch.Chapter.objects(chapter=doc).first() # type: ignore
​                chapter_filepath = chapter_doc.html_path
​                files.append(chapter_filepath)
​                progress.update(filenames_task, advance=1)  # Update Progress Bar



def save_default_files(section: int, part: int, files: List[str]) -> None:
    """
    Save the list of the file's filenames contained in a given section.

​    Args:
​        `section` (sec.Section): the given section.

​        `files` (List[str]): The list of filenames/filepaths contained in the given section.

​    Raises:
​        `ValueError`: The given section doesn't exist in MongoDB.

​    Returns:
​        `files` (List[str] | List[Path]): The list of filenames/filepaths contained in the given section.
​    """
​    sg()
​    doc = Default.objects(section=section).first()  # type: ignore
​    book = sec.get_section_book(section)
​    match part:
​        case 0 | 1:
​            doc.section1_files = files
​            key = "section1_files"
​            panel_key = f"Book {book}'s first sections's files"
​        case 2:
​            doc.section2_files = files
​            key = "section2_files"
​            panel_key = f"Book {book}'s second sections's files"
​        case _:
​            raise ValueError(f"Section {section} is not a valid section.")
​    doc.save()

​    log.debug(f"Saved Book {book}'s default doc's {key}:\n\n {files}")

​    console.print(
​        default_panel(section, panel_key, ",\n".join(files), 645), highlight=True
​    )


def get_section_files(section: int):
    sg()
    for doc in sect.Section.objects(section=section):
        return doc.section_files


# . Verified
def generate_input_files_single(book: int, save: bool = False):
    """
    Generates a list of input files of a given book.

​    Args:
​        `book` (int):
​            The given book.

​    Raises:
​        `ValueError`:
​            Invalid Book Input. Valid books are 1, 2, and 3.

​    Returns:
​        `input_files` (list[str]):
​            The input files of a given book.
​    """
​    valid_books = [1, 2, 3]
​    if book in valid_books:
​        book_str = str(book).zfill(2)
​        input_files = [f"cover{book}.html", f"titlepage-{book_str}.html"]
​        section_files = generate_section_files(book)
​        input_files.extend(section_files)
​        input_files.append(f"endofbook-{book_str}.html")
​        if save:
​            sg()
​            for doc in Defaultdoc.objects(book=book):
​                doc.input_files = input_files
​                doc.save()
​        return input_files
​    else:
​        raise ValueError(f"Invalid book: {book}\n\nValid books are 1, 2, and 3.")


# . Verified
def generate_input_files_multiple(book: int, save: bool = False):
    """
    Generates a list of input files of a given book.

​    Args:
​        `book` (int):
​            The given book.

​    Raises:
​        `ValueError`:
​            Invalid Book Input. Valid books are 4-10.

​    Returns:
​        `input_files` (list[str]):
​            The input files of a given book.
​    """
​    valid_books = [4, 5, 6, 7, 8, 9, 10]
​    if book not in valid_books:
​        raise ValueError(f"Invalid book: {book}\n\nValid books are 4-10.")
​    input_files = []
​    for doc in Defaultdoc.objects(book=book):
​        book_str = str(book).zfill(2)
​        input_files.append(f"cover{book}.html")
​        input_files.append(f"titlepage-{book_str}.html")
​        sections = doc.sections
​        log.debug(f"Book {book}'s sections: {sections}")
​        for section in sections:
​            section_files = generate_section_files(section)
​            input_files.extend(section_files)
​        input_files.append(f"endofbook-{book_str}.html")

​        result = f"Book {book}'s files:\n"
​        for item in input_files:
​            result += f"- {item}\n"

​        log.debug(result)

​    if save:
​        sg()
​        for doc in Defaultdoc.objects(book=book):
​            doc.input_files = input_files
​            doc.save()
​    return input_files


def get_input_files(book: int):
    """
    Retrieve a given book's input files from MongoDB.

​    Args:
​        `book` (int)
​            The given book

​    Returns:
​        `input_files` (list[str]):
​            The given book's input files.
​    """
​    sg()
​    for doc in Defaultdoc.objects(book=book):
​        return doc.input_files


def generate_resource_paths(book: int, save: bool = False):
    book_str = str(book).zfill(2)
    book_dir = f"${{.}}"
    resource_files = ["."]

    # > Non-content files
    # Images
​    resource_files.append(f"{book_dir}/Images/cover{book}.png")
​    resource_files.append(f"{book_dir}/Images/title.png")
​    resource_files.append(f"{book_dir}/Images/gem.gif")

    # Fonts
​    resource_files.append(f"{book_dir}/Styles/Urbanist-Regular.ttf")
​    resource_files.append(f"{book_dir}/Styles/Urbanist-Thin.ttf")
​    resource_files.append(f"{book_dir}/Styles/Urbanist-Italit.ttf")
​    resource_files.append(f"{book_dir}/Styles/Urbanist-ThinItalic.ttf")
​    resource_files.append(f"{book_dir}/Styles/White Modestry.ttf")

    # CSS
​    resource_files.append(f"{book_dir}/Styles/style.css")

    # Metadata
​    resource_files.append(f"{book_dir}/yaml/meta{book}.yml")
​    resource_files.append(f"{book_dir}/yaml/epub-meta{book}.yml")

    # > Content files
​    sg()
​    for doc in Defaultdoc.objects(book=book):
​        input_files = doc.input_files
​        for input_file in input_files:
​            resource_files.append(f"{book_dir}/html/{input_file}")

​    result = f"Book {book}'s resource files:\n"
​    for resource in resource_files:
​        result += f"- {resource}\n"

​    log.debug(result)

​    if save:
​        sg()
​        for doc in Defaultdoc.objects(book=book):
​            doc.resource_paths = resource_files
​            doc.save()

​    log.debug(f"Finished generating resource files for book {book}.")

​    return resource_files


def get_resource_paths(book: int):
    """
    Retrieve a given book's resource files from MongoDB.

​    Args:
​        `book` (int)
​            The given book):

​    Returns:
​        `resource_paths` (list[str]):
​            The given book's resource files.
​    """
​    sg()
​    for doc in Defaultdoc.objects(book=book):
​        return doc.resource_paths


def load_meta(book: int):
    """
    Loads the metadata of a given book from MongoDB.

​    Args:
​        `book` (int)
​            The given book):

​    Returns:
​        `meta` (dict):
​            The given book's metadata.
​    """
​    sg()
​    for doc in meta.Metadata.objects(book=book):
​        metadata = doc.text
​        log.debug(f"Retrieved Metadata for Book {book}:\n\n {metadata}")
​    sg()
​    for doc in epubmeta.Epubmeta.objects(book=book):
​        epub_metadata = doc.text
​        log.debug(f"Retrieved ePub Metadata for Book {book}:\n\n {epub_metadata}")
​    sg()
​    for doc in Defaultdoc.objects(book=book):
​        doc.metadata = metadata
​        doc.epubmetadata = epub_metadata
​        doc.save()
​        log.debug(f"Updated Book {book}'s defualtdoc with Metadata and ePub Metadata.")


def generate_default_doc_f(book: int, save: bool = False):
    """
    Generates the default doc for a given book.

​    Args:
​        `book` (int):
​            The given book.

​    Raises:
​        `ValueError`:
​            Invalid Book Input. Valid books are 1-10.

​    Returns:
​        `default_doc` (dict):
​            The default doc for a given book.
​    """
    # > Validate book
​    valid_books = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
​    if book not in valid_books:
​        raise InvalidBookError(f"Invalid book: {book}\nValid books are 1-10.")

​    sg()
​    mongodefault = Defaultdoc.objects(book=book).first()
​    output = mongodefault.output

​    default_1 = f"from: html\nto: epub\n  \noutput-file: {output}"

​    input_file_list = mongodefault.input_files
​    input_files = f"\n  \ninput-files:\n"
​    for file in input_file_list:
​        input_files = f"{input_files}\n- {file}"

​    default3 = f"\n\nstandalone: true\nself-contained: true\n"

​    resource_files = "resource-files:\n- ."
​    resource_file_list = mongodefault.resource_paths
​    for file in resource_file_list:
​        resource_files = f"{resource_files}\n- {file}"

​    epub = f"toc: true\ntoc-depth: 2\nepub-chapter-level: 2\nepub-cover-image: cover{book}.png\n  "

​    fonts = f"\nepub-fonts:\n- Urbanist-Italic.ttf\n- Urbanist-Regular.ttf\n- Urbanist-Thin.ttf\n- Urbanist-ThinItalic.ttf\n- White Modesty.ttf\n"

​    meta = f"epub-metadata: {mongodefault.epubmetadata}\nmetadata-files:\n- meta{book}.yml\n- epub-meta{book}.yml\n"

​    css = "css-files:\n- style.css\n"

​    default_doc = f"{default_1}\n{input_files}\n{default3}\n{resource_files}\n{epub}\n{fonts}\n{meta}\n{css}"

​    filepath = mongodefault.filepath
​    yaml_str = myaml.dump(default_doc)
​    with open(filepath, "w") as outfile:
​        outfile.write(yaml_str)

​    if save:
​        sg()
​        default_mongo_doc = Defaultdoc.objects(book=book).first()
​        default_mongo_doc.default_doc = default_doc
​        default_mongo_doc.save()
​        log.debug(f"Updated Book {book}'s defualtdoc with default doc.")
​    return default_doc


def generate_cover(book: int, save: bool = False):
    cover = f"cover{book}.png"
    if save:
        sg()
        doc = Defaultdoc.objects(book=book).first()
        doc.cover = cover
        doc.save()
    return cover


def generate_cover_path(book: int, save: bool = False):
    sg()
    for doc in Defaultdoc.objects(book=book):
        book = doc.book
        book_str = str(book).zfill(2)
        book_dir = f"book{book_str}"
        cover_path = f"{BASE}/books/{book_dir}/Images/cover{book}.png"

​        if save:
​            doc.cover_path = cover_path
​            doc.save()

​        return cover_path


def generate_title(book: int, save: bool = False):
    """
    Generates the default doc for a given book.

​    Args:
​        `book` (int):
​            The given book.
​        `save` (bool):
​            Whether or not to save the default doc to MongoDB.
​        `write` (bool):
​            Whether or not to write the default doc to a file.

​    Raises:
​        `ValueError`:
​            Invalid Book Input. Valid books are 1-10.

​    Returns:
​        `default_doc` (dict):
​            The default doc for a given book.
​    """
​    bar_title = f"Generating title for Book {book}"
​    bar_title_length = len(bar_title)
​    title_length = bar_title_length + 1
​    sg()
​    doc = book_.Book.objects(book=book).first()
​    if doc is None:
​        raise InvalidBookError(f"Invalid book: {book}\nValid books are 1-10.")

​    title = doc.title
​    log.debug(f"Retrieved title for Book {book}")

​    if save:
​        sg()
​        default_ = Defaultdoc.objects(book=book).first()
​        default_.title = title
​        default_.save()
​        log.debug(f"Updated Book {book}'s defualtdoc with title.")

​    return title


def get_input_files(book: int) -> str:
    sg()
    doc = Defaultdoc.objects(book=book).first()
    inputf = "input-files:"
    for file in doc.input_files:
        inputf = f"{inputf}\n- {file}"
    log.debug(f"Retrieved input files for Book {book}:</code>\n{inputf}</code>")
    return inputf


def get_resource_path(book: int) -> str:
    sg()
    doc = Defaultdoc.objects(book=1).first()
    resourcef = "resource-files:"
    for file in doc.resource_paths:
        resourcef = f"{resourcef}\n- {file}"
    log.debug(f"Retrieved resource path for Book {book}:</code>\n{resourcef}</code>")
    return resourcef


def generate_default_doc(book: int, save: bool = True, write: bool = True):
    sg()
    doc = Defaultdoc.objects(book=book).first()

    # . Read default variable from MongoDB
    # > Book
​    book = doc.book
​    book_str = str(book).zfill(2)
​    book_dir = f"book{book_str}"

    # > Output
​    output = doc.output
​    title = doc.title

    # > Book Word
​    book_word = doc.book_word

    # > Cover
​    cover = doc.cover
​    cover_path = doc.cover_path

    # > Filename and Path
​    filepath = doc.filepath

    # > Input FIles
​    input_files = get_input_files(book)

    # > Resource_Files
​    resource_path = get_resource_path(book)

    # > Epub
​    epubmetadata = doc.epubmetadata
    # > Metadata
​    metadata = doc.metadata

    # > CSS
​    css = "css:\n- style.css\n..."

    # > Default Doc
​    default = f"---\nfrom: html\nto: epub\n\n"
​    default = f"{default}\output-file: {book} - {title}.epub\n"

    # > Input Files
​    default = f"{default}\n{input_files}\n"

    # > Mid
​    default = f"{default}\nstandalone: true\nself-contained: true\n"

    # > Resource Path
​    default = f"{default}\n{resource_path}"

    # > toc
​    default = f"{default}\n\ntoc: true\ntoc-depth: 2\n\nepub-chapter-level: 2\nepub-cover-image: {cover}\n"

    # > epubfonts
​    default = f"{default}\nepub-fonts:\n- Urbanist-Italic.ttf\n- Urbanist-Regular.ttf\n- Urbanist-Thin.ttf\n- Urbanist-ThinItalic.ttf\n- White Modesty.ttf\n"

    # >Meta
​    default = f"{default}\nepub-metadata: epub-meta{book}.yml\n\nmetadata-files:\n- meta{book}.yml\n- epub-meta{book}.yml\n"

    # > CSS
​    default = f"{default}\ncss-files:\n- style.css\n..."

    # > Default Doc
​    log.debug(default)

    # > Filepath
​    if write:

​        filepath = doc.filepath
​        with open(filepath, "w") as outfile:
​            outfile.write(default)
​        log.debug(f"Saved Book {book}'s defualtdoc to disk.")

    # > Save
​    if save:
​        sg()
​        default_mongo_doc = Defaultdoc.objects(book=book).first()
​        default_mongo_doc.default_doc = default
​        default_mongo_doc.save()
​        log.debug(f"Updated MongoDB with Book {book}'s defualt file.")
​    return default


# for i in trange(1,11):
#     generate_default_doc(i, save=True, write=True)