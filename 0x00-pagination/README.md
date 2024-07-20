 # 0x00-pagination

## Description

This directory contains the implementation of a pagination system for managing large datasets. The system is designed to split data into manageable pages, enabling efficient navigation and retrieval of information. The pagination system is implemented in Python and provides functions to handle various operations related to pagination, such as fetching a specific page of data, navigating between pages, and customizing the number of items per page.

The main features of the pagination system include:

- Dynamic Page Navigation: Easily move between pages of data.
- Customizable Page Size: Adjust the number of items displayed per page.
- Data Handling: Efficiently manage large datasets by breaking them into smaller, more manageable chunks.

## Directory Structure

- pagination.py: The main module containing the implementation of the pagination system.
- test_pagination.py: Test cases to validate the functionality of the pagination system.
- data/: A directory containing sample datasets used for testing the pagination system.
- README.md: This file, providing an overview and description of the directory and its contents.

## Usage

1. Initialization:
Initialize the pagination system with your dataset and specify the number of items per page.

      from pagination import Paginator

      dataset = [1, 2, 3, ..., 100]  # Example dataset
      paginator = Paginator(dataset, items_per_page=10)

2. Fetching Pages:
Retrieve a specific page of data.

      page_data = paginator.get_page(1)  # Get the first page

3. Navigating Pages:
Move to the next or previous page.

      next_page = paginator.next_page()
      previous_page = paginator.previous_page()

4. Customizing Page Size:
Change the number of items per page.

      paginator.set_items_per_page(20)

## Testing

To run the test cases and validate the functionality of the pagination system, execute the following command:

      python -m unittest test_pagination.py

## Contributing

Contributions to enhance the pagination system are welcome. Please follow the standard GitHub workflow:

1. Fork the repository.
2. Create a new branch.
3. Make your changes.
4. Submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

