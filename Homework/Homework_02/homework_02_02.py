library = {
    "1984": {"author": "George Orwell", "year": 1949, "genre": "Dystopian"},
    "1984_2": {"author": "George Orwell", "year": 1949, "genre": "Dystopian"},
    "To Kill a Mockingbird": {
        "author": "Harper Lee",
        "year": 1960,
        "genre": "Southern Gothic",
    },
    "The Great Gatsby": {
        "author": "F. Scott Fitzgerald",
        "year": 1925,
        "genre": "Tragedy",
    },
    "Moby Dick": {"author": "Herman Melville", "year": 1851, "genre": "Adventure"},
    "War and Peace": {
        "author": "Leo Tolstoy",
        "year": 1869,
        "genre": "Historical Fiction",
    },
    "Pride and Prejudice": {"author": "Jane Austen", "year": 1813, "genre": "Romance"},
    "Brave New World": {
        "author": "Aldous Huxley",
        "year": 1932,
        "genre": "Science Fiction",
    },
    "The Catcher in the Rye": {
        "author": "J.D. Salinger",
        "year": 1951,
        "genre": "Realist Fiction",
    },
    "The Lord of the Rings": {
        "author": "J.R.R. Tolkien",
        "year": 1954,
        "genre": "Fantasy",
    },
    "The Hobbit": {"author": "J.R.R. Tolkien", "year": 1937, "genre": "Fantasy"},
    "The Odyssey": {"author": "Homer", "year": -800, "genre": "Epic Poetry"},
    "Crime and Punishment": {
        "author": "Fyodor Dostoevsky",
        "year": 1866,
        "genre": "Psychological Fiction",
    },
    "The Brothers Karamazov": {
        "author": "Fyodor Dostoevsky",
        "year": 1880,
        "genre": "Philosophical Fiction",
    },
    "Jane Eyre": {
        "author": "Charlotte Brontë",
        "year": 1847,
        "genre": "Gothic Fiction",
    },
    "The Divine Comedy": {
        "author": "Dante Alighieri",
        "year": 1320,
        "genre": "Epic Poetry",
    },
    "Don Quixote": {"author": "Miguel de Cervantes", "year": 1605, "genre": "Satire"},
    "Ulysses": {"author": "James Joyce", "year": 1922, "genre": "Modernist Fiction"},
    "Frankenstein": {"author": "Mary Shelley", "year": 1818, "genre": "Gothic Fiction"},
    "The Iliad": {"author": "Homer", "year": -762, "genre": "Epic Poetry"},
    "Madame Bovary": {"author": "Gustave Flaubert", "year": 1856, "genre": "Realism"},
}

sortedLibrary = sorted(library.items(), key=lambda item: item[1]["year"])
print(sortedLibrary)