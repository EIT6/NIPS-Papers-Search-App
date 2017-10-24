import React, { Component } from 'react'
import extend from 'lodash/extend'
import { SearchkitManager,SearchkitProvider,
  SearchBox, RefinementListFilter, Pagination,
  HierarchicalMenuFilter, HitsStats, SortingSelector, NoHits,
  ResetFilters, RangeFilter, NumericRefinementListFilter,
  ViewSwitcherHits, ViewSwitcherToggle, DynamicRangeFilter,
  InputFilter, GroupedSelectedFilters,
  Layout, TopBar, LayoutBody, LayoutResults,
  ActionBar, ActionBarRow, SideBar } from 'searchkit'
import './index.css'

const host = "http://95.85.30.94/es/papers/"
const searchkit = new SearchkitManager(host)

const PaperHitsGridItem = (props)=> {
  const {bemBlocks, result} = props
  let url = "https://papers.nips.cc/paper/" + result._source.pdf_name.split(".pdf")[0]
  const source = extend({}, result._source, result.highlight)
  return (
    <div className={bemBlocks.item().mix(bemBlocks.container("item"))} data-qa="hit">
      <a href={url} target="_blank">
        
        <div data-qa="title" className={bemBlocks.item("title")} dangerouslySetInnerHTML={{__html:source.title}}></div>
      </a>
    </div>
  )
}

const PaperHitsListItem = (props)=> {
  const {bemBlocks, result} = props
  let url = "https://papers.nips.cc/paper/" + result._source.pdf_name.split(".pdf")[0] 
  const source = extend({}, result._source, result.highlight)
  return (
    <div className={bemBlocks.item().mix(bemBlocks.container("item"))} data-qa="hit">
      <div className={bemBlocks.item("poster")}>
      </div>
      <div className={bemBlocks.item("details")}>
        <a href={url} target="_blank"><h1 className={bemBlocks.item("title")} dangerouslySetInnerHTML={{__html:source.title}}></h1></a>
        <h4 className={bemBlocks.item("subtitle")}>By {source.authors.join(", ")}. Released in {source.year}. Has been cited {source.citations} times in NIPS proceedings.</h4>
        <h4>Top Keywords (In order of Importance):</h4>
        <div className={bemBlocks.item("text")} dangerouslySetInnerHTML={{__html:source.keywords.join(", ")}}></div>
        <h4>Abstract:</h4>
        <div className={bemBlocks.item("text")} dangerouslySetInnerHTML={{__html:source.abstract}}></div>
      </div>
    </div>
  )
}
//TODO field weights
class App extends Component {
  render() {
    return (
      <SearchkitProvider searchkit={searchkit}>
        <Layout>
          <TopBar>
            <div className="my-logo">NIPS Papers IR System</div>
            <SearchBox autofocus={true} searchOnChange={true} prefixQueryFields={["abstract^1","title^2"]}/>
          </TopBar>
        <LayoutBody>

          <SideBar>
            <RangeFilter min={0} max={53} field="citations" id="citations" title="Citation Counts" showHistogram={true}/>
            <RangeFilter min={1987} max={2017} field="year" id="year" title="Publication Year" showHistogram={true}/>
            <RefinementListFilter id="authors" title="Authors" field="authors.raw" size={10}/>

            <HierarchicalMenuFilter fields={["type.raw", "genres.raw"]} title="Categories" id="categories"/>
            <DynamicRangeFilter field="metaScore" id="metascore" title="Metascore" rangeFormatter={(count)=> count + "*"}/>
            <RangeFilter min={0} max={10} field="imdbRating" id="imdbRating" title="IMDB Rating" showHistogram={true}/>
            <InputFilter id="authors-search" searchThrottleTime={500} title="Authors" placeholder="Search authors" searchOnChange={true} queryFields={["authors"]} />
            <RefinementListFilter id="writersFacets" translations={{"facets.view_more":"View more writers"}} title="Writers" field="writers.raw" operator="OR" size={10}/>
            <RefinementListFilter id="countries" title="Countries" field="countries.raw" operator="OR" size={10}/>
            <NumericRefinementListFilter id="runtimeMinutes" title="Length" field="runtimeMinutes" options={[
              {title:"All"},
              {title:"up to 20", from:0, to:20},
              {title:"21 to 60", from:21, to:60},
              {title:"60 or more", from:61, to:1000}
            ]}/>
          </SideBar>
          <LayoutResults>
            <ActionBar>

              <ActionBarRow>
                <HitsStats translations={{
                  "hitstats.results_found":"{hitCount} results found"
                }}/>
                <ViewSwitcherToggle/>
                <SortingSelector options={[
                  {label:"Relevance", field:"_score", order:"desc"},
                  {label:"Latest Publications", field:"year", order:"desc"},
                  {label:"Earliest Publications", field:"year", order:"asc"},
                  {label:"Most Citations", field:"citations", order:"desc"}                     
                ]}/>
              </ActionBarRow>

              <ActionBarRow>
                <GroupedSelectedFilters/>
                <ResetFilters/>
              </ActionBarRow>

            </ActionBar>
            <ViewSwitcherHits
                hitsPerPage={12} highlightFields={["title","citations"]}
                sourceFilter={["abstract", "authors", "citations", "pdf_name", "title", "year", "top_keywords"]}
                hitComponents={[
                  {key:"list", title:"List", itemComponent:PaperHitsListItem, defaultOption:true},
                  {key:"grid", title:"Grid", itemComponent:PaperHitsGridItem}
                ]}
                scrollTo="body"
            />
            <NoHits suggestionsField={"title"}/>
            <Pagination showNumbers={true}/>
          </LayoutResults>

          </LayoutBody>
        </Layout>
      </SearchkitProvider>
    );
  }
}

export default App;
