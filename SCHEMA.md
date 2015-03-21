# Schema


Why not use PostgreSQL?


## Table `taxon`

| Column              | Type            | Attributes                        |
| ------------------- | --------------- | --------------------------------- |
| `id`                | `integer`       | `primary key`, `not null`         |
| `scientific_name`   | `varchar(1024)` | `unique`, `not null`, "final"     |
| `rank_id`           | `integer`       | `foreign(rank.id)`, `not null`    |
| `parent_id`         | `integer`       | `foreign(taxon.id)`               |
| `authority`         | `varchar(1024)` |                                   |
| `organism`          | `enum(...)`     | `not null`                        |
| `created_at`        | `datetime`      | `not null`                        |
| `updated_at`        | `datetime`      |                                   |

- `enum('organism_enum', 'animal', 'bacterial', 'fungi', 'plant', 'protist', 'virus')`
  https://en.wikipedia.org/wiki/Category:Systems_of_taxonomy_by_organism


## Table `rank`

| Column              | Type            | Attributes                        |
| ------------------- | --------------- | --------------------------------- |
| `id`                | `integer`       | `primary key`, `not null`         |
| `name`              | `varchar(1024)` | `not null`                        |
| `organism`          | `enum(...)`     |                                   |


## Table `system`

| Column              | Type            | Attributes                        |
| ------------------- | --------------- | --------------------------------- |
| `id`                | `integer`       | `primary key`, `not null`         |
| `name`              | `varchar(1024)` | `not null`                        |
| `organism`          | `enum(...)`     | `not null`                        |
| `published_at`      | `datetime`      | `not null`                        |


## Table `taxon_system`

| Column              | Type            | Attributes                        |
| ------------------- | --------------- | --------------------------------- |
| `id`                | `integer`       | `primary key`, `not null`         |
| `taxon_id`          | `integer`       | `foreign(taxon.id)`, `not null`   |
| `system_id`         | `integer`       | `foreign(system.id)`              |
| `another_taxon_id`  | `integer`       | `foreign(taxon.id)`               |
| `another_taxon_type`| `enum(...)`     |                                   |
| `is_recognized`     | `boolean`       | `not null`                        |

- `enum('another_taxon_type_enum', 'parent', 'sibling')`


## Table `taxon_alias`

| Column              | Type            | Attributes                        |
| ------------------- | --------------- | --------------------------------- |
| `id`                | `integer`       | `primary key`, `not null`         |
| `taxon_id`          | `integer`       | `foreign(taxon.id)`, `not null`   |
| `language`          | `enum(...)`     | `not null`                        |
| `is_primary`        | `boolean`       | `not null`                        |
| `name`              | `varchar(1024)` | `not null`                        |

- `unique(taxon_id, is_primary)`
- `enum('taxon_alias_language_enum', 'en', 'zh-cn', 'zh-tw', 'zh-hk')`


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
- extend authority
- extinct?
- references
- taxon description
- taxon revision tag (for review)
