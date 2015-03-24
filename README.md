# taxon
A taxonomy website for Chinese

# TODO list

- [x] Use SQLAlchemyUtils and Arrow
- [ ] Update database schema according to ITIS database
 - [x] Rough but runnable script
 - [ ] Disable auto-increment on rank.id
- [ ] Add missing schema (described in SCHEMA.md)
- [ ] Views for showing and editing taxonomy data (TaxonView)
 - [ ] Adjust views, templates and models affected due to schema changing
 - [ ] Basic templates for showing
 - [ ] Taxon parent (auto-complate input)
 - [ ] Place for adding alias names
 - [ ] Only can be edited by authorized users
- [ ] Views for adding/editing system
- [ ] Views for indexing taxa (TaxaView)
- [ ] Homepage View (HomeView)
- [ ] I18n support
- [ ] Fake data generator (for development and testing)
- [ ] Revision functions and views
- [ ] OAuth support (use Chinese Wikipedia as OAuth server)
- [ ] Account support (or just OAuth?)
- [ ] Autobot
 - [ ] Import existing taxonomy data from Wikipedia and other sources
 - [ ] Import existing Chinese translation from web sources
- [ ] Allow authorized users to export their contribution to Chinese Wikipedia
- [ ] Support name querying (both Chinese and scientific name)
