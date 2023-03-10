# Newsela test

This is a ETL pipeline developed using Prefect Tasks and Flows. It follows a simple approach extracting articles from a predefined source: [The Guardian](https://open-platform.theguardian.com/), applies simple transformations to the retrieved articles, and stores the processed information into a Postgresql database.
## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

## Usage

The entry point is the `manage.py` file. It is prepared to trigger different pipelines from the terminal using the parameter `source`. The parameter source must match the name of the package created in the `pipelines` folder for a given source.

```bash
python manage.py -s the_guardian
```

As a result of the execution of the pipeline, the processed recrods are stored in a Postgresql database. For evaluation purposes, a Docker container with a simple database is enabled trough `docker-compose`. To start the database execute the following command:

```bash
docker-compose up -d
```

## Queries

```sql
SELECT section, COUNT(*) AS articles_count, AVG(word_count) AS word_count_avg
FROM articles
GROUP BY section
```

```sql
SELECT date_trunc('MONTH', created_at) AS period, COUNT(*) AS articles_count
FROM articles
GROUP BY date_trunc('MONTH', created_at)
```


## License

[MIT](https://choosealicense.com/licenses/mit/)