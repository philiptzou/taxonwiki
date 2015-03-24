# Schema


Why not use PostgreSQL?


## Table `taxon`

| Column              | Type            | Attributes                        |
| ------------------- | --------------- | --------------------------------- |
| `id`                | `integer`       | `primary key`, `not null`         |
| `scientific_name`   | `varchar(1024)` | `unique`, `not null`              |
| `rank`              | `choice(...)`   | `not null`                        |
| `parent_id`         | `integer`       | `foreign(taxon.id)`               |
| `author_abbr`       | `varchar(1024)` |                                   |
| `organism`          | `choice(...)`   | `not null`                        |
| `created_at`        | `datetime`      | `not null`                        |
| `updated_at`        | `datetime`      |                                   |

- `organism` = `choice('animal', 'bacterial', 'fungi', 'plant', 'protist', 'virus')`
  https://en.wikipedia.org/wiki/Category:Systems_of_taxonomy_by_organism


## Table `author`

| Column              | Type            | Attributes                        |
| ------------------- | --------------- | --------------------------------- |
| `id`                | `integer`       | `primary key`, `not null`         |
| `name`              | `varchar(1024)` | `not null`                        |
| `name_vector`       | `TSVector(name)`|                                   |


## Table `taxon_author`

| Column              | Type            | Attributes                        |
| ------------------- | --------------- | --------------------------------- |
| `id`                | `big_integer`   | `primary key`, `not null`         |
| `taxon_id`          | `integer`       | `foreign(taxon.id)`, `not null`   |
| `author_id`         | `integer`       | `foreign(author.id)`, `not null`  |
| `year`              | `integer`       |                                   |


## Table `system`

| Column              | Type            | Attributes                        |
| ------------------- | --------------- | --------------------------------- |
| `id`                | `integer`       | `primary key`, `not null`         |
| `name`              | `varchar(1024)` | `not null`                        |
| `organism`          | `choice(...)`   | `not null`                        |
| `published_at`      | `datetime`      | `not null`                        |


## Table `taxon_system`

| Column              | Type            | Attributes                        |
| ------------------- | --------------- | --------------------------------- |
| `id`                | `integer`       | `primary key`, `not null`         |
| `taxon_id`          | `integer`       | `foreign(taxon.id)`, `not null`   |
| `system_id`         | `integer`       | `foreign(system.id)`, `not null`  |
| `another_taxon_id`  | `integer`       | `foreign(taxon.id)`               |
| `another_taxon_type`| `enum(...)`     |                                   |
| `is_recognized`     | `boolean`       | `not null`                        |

- `enum('another_taxon_type_enum', 'parent', 'sibling')`


## Table `taxon_alias`

| Column              | Type            | Attributes                        |
| ------------------- | --------------- | --------------------------------- |
| `id`                | `integer`       | `primary key`, `not null`         |
| `taxon_id`          | `integer`       | `foreign(taxon.id)`, `not null`   |
| `language`          | `choice(...)`   | `not null`                        |
| `is_primary`        | `boolean`       | `not null`                        |
| `name`              | `varchar(1024)` | `not null`                        |

- `unique(taxon_id, is_primary)`
- `language` = `choice('en', 'zh-cn', 'zh-tw', 'zh-hk')`


## Table `taxon_revision`

| Column              | Type            | Attributes                        |
| ------------------- | --------------- | --------------------------------- |
| `id`                | `big_integer`   | `primary key`, `not null`         |
| `taxon_id`          | `integer`       | `foreign(taxon.id)`, `not null`   |
| `contributor_id`    | `integer`       | `not null`                        |
| `body`              | `JSON`          |                                   |
| `comment`           | `varchar(1024)  |                                   |
| `created_at`        | `datetime`      | `not null`                        |

## TODO

- contributor
- extinct?
- references
- taxon description
- taxon revision tag (for review)
