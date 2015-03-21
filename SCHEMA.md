# Schema


Why not use PostgreSQL?


## Table `taxa`

| Column              | Type            | Attributes                        |
| ------------------- | --------------- | --------------------------------- |
| `id`                | `integer`       | `primary key`, `not null`         |
| `scientific_name`   | `varchar(1024)` | `unique`, `not null`, "final"     |
| `rank_id`           | `integer`       | `foreign(rank.id)`, `not null`    |
| `parent_id`         | `integer`       | `foreign(taxa.id)`                |
| `authority`         | `varchar(1024)` |                                   |
| `organism`          | `enum(...)`     | `not null`                        |
| `created_at`        | `datetime`      | `not null`                        |
| `updated_at`        | `datetime`      |                                   |


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


## Table `taxa_discontinued`

| Column              | Type            | Attributes                        |
| ------------------- | --------------- | --------------------------------- |
| `id`                | `integer`       | `primary key`, `not null`         |
| `taxa_id`           | `integer`       | `foreign(taxa.id)`, `not null`    |
| `system_id`         | `integer`       | `foreign(system.id)`              |
| `another_taxa_id`   | `integer`       | `foreign(taxa.id)`                |
| `another_taxa_type` | `enum(...)`     |                                   |
| `is_valid`          | `boolean`       | `not null`                        |

- `enum('taxa_discontinued_another_taxa_type', 'parent', 'sibling')`


## Table `taxa_system`

| Column              | Type            | Attributes                        |
| ------------------- | --------------- | --------------------------------- |
| `id`                | `integer`       | `primary key`, `not null`         |
| `taxa_id`           | `integer`       | `foreign(taxa.id)`, `not null`    |
| `system_id`         | `integer`       | `foreign(system.id)`, `not null`  |


## Table `taxa_alias_name`

| Column              | Type            | Attributes                        |
| ------------------- | --------------- | --------------------------------- |
| `id`                | `integer`       | `primary key`, `not null`         |
| `taxa_id`           | `integer`       | `foreign(taxa.id)`, `not null`    |
| `language`          | `enum(...)`     | `not null`                        |
| `is_primary`        | `boolean`       | `not null`                        |
| `name`              | `varchar(1024)` | `not null`                        |

- `unique(taxa_id, is_primary)`
- `enum('taxa_alias_name_language', 'en', 'zh-cn', 'zh-tw', 'zh-hk')`


## Table `taxa_revision`

| Column              | Type            | Attributes                        |
| ------------------- | --------------- | --------------------------------- |
| `id`                | `integer`       | `primary key`, `not null`         |
| `taxa_id`           | `integer`       | `foreign(taxa.id)`, `not null`    |
| `contributor_id`    | `integer`       | `not null`                        |
| `body`              | `JSON`          |                                   |
| `comment`           | `varchar(1024)  |                                   |
| `created_at`        | `datetime`      | `not null`                        |

## TODO

- extinct?
- references
- taxa description
- taxa revision tag (for review)
