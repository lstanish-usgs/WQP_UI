// Portal / Data Download Tooltips

export class TOOLTIP {
    static get countryTooltip() { return '<center>Select one or multiple <strong><em>countries</em></strong> represented in the database. Parentheses <br>after each country represent which database(s) it is represented in.</center>';}
    static get stateTooltip() { return '<center>Select one or multiple <strong><em>states</em></strong>. Parentheses after each <br>state represent which database(s) it is represented in.</center>';}
    static get countyTooltip() { return '<center>Select one or multiple <strong><em>counties</em></strong> from the selected state(s). Parentheses <br>after each county represent which database(s) it is represented in.<center>';}
    static get pointLocationTooltip() { return '<center>Enter <em>latitude</em> and <em>longitude</em> (<strong>decimal degrees</strong> referenced to NAD83), and <em>radial <br>distance</em> (<strong>miles</strong>) to create a <strong><em>search area</em></strong>. Longitudes in the western hemisphere <br>begin with a negative sign. Many stations outside the continental US do not have latitude <br>and longitude referenced to NAD83 and cannot be found using these parameters. <br><em>Example:</em> Within: <strong>20</strong> miles of Latitude: <strong>46.12</strong> Longitude: <strong>-89.15</strong></center>';}
    static get boundingBoxTooltip() { return '<center>Enter the North and South <em>latitudes</em> and the East and West <em>longitudes</em> <br>(<strong>decimal degrees</strong> referenced to NAD83) to create a <strong><em>bounding box</em></strong>. <br>Longitudes in the western hemisphere should begin with a negative sign. <br><em>Example:</em> North: <strong>46.12</strong>, East: <strong>-89.15</strong>, South: <strong>45.93</strong>, West: <strong>-89.68</strong></center>';}
    static get siteTypeTooltip() { return '<center><strong><em>Site type</em></strong> indicates a <em>natural</em> or <em>human-made</em> feature affecting the hydrologic <br>conditions measured at a site. Select one or multiple site types. Parentheses <br>after each site type represent which database(s) it is represented in.</center>';}
    static get orgIDTooltip() { return '<center>Identifies a unique <strong><em>business</em></strong> or <strong><em>company</em></strong>. Select one or multiple organization <br>IDs. Type at least two characters for a list to appear. For more information <br>on Water Quality Exchange (WQX) Organization IDs, see <a href="https://www.epa.gov/waterdata/water-quality-data">About EPA/WQX</a></center>';}
    static get siteIDTooltip() { return '<center>Identifies a <strong><em>monitoring location</em></strong> by a unique name, number, or code. Select <br>one or multiple site IDs. Type at least two characters for a list to appear. <br><em>Examples:</em> For NWIS site: <strong>USGS-301650089215300</strong> <br>For EPA site: <strong>R10BUNKER-CUA005-5</strong></center>';}
    static get hucTooltip() { return '<center>Identifies the <strong><em>hydrological unit</em></strong> up to the cataloging unit level of precision. <br>Select one or multiple HUC IDs. Separate multiple HUC IDs with a <br><strong>semicolon</strong> (";"). Select partial HUCs using <strong>trailing wildcards</strong> ("*"). <br><em>Examples:</em> One site: <strong>01010005</strong> <br>Multiple sites: <strong>01010003;01010004</strong> <br>Partial HUCs: <strong>010801*</strong></center>';}
    static get minSamplingTooltip() { return '<center>Returns only sites where at least a minimum number of <strong><em>sampling <br>activities</em></strong> have been reported. Select a value; the default is <strong>1</strong>.</center>';}
    static get upDownStreamTooltip() { return '<center>Click the Expand button in the upper right of the map. This will show a larger map. Zoom in to see features of interest. The feature source can be changed using the feature select picker in the upper right. Click on a feature to display a popup dialog where you enter the navigation type and optional distance. Then click the Navigate button to show the sites upstream or downstream from the feature. Use a distance with upstream tributaries to restrict the query size and ensure that the result does not crash the page. This tool uses the Network Linked Data Index to navigate.</center>';}
    static get sampleMediaTooltip() { return '<center>Identifies the <strong><em>environmental medium</em></strong> where a sample was taken. <br>Select one or multiple sample media types. Parentheses after each <br>sample medium represent which database(s) it is represented in.</center>';}
    static get charGroupTooltip() { return '<center>Groups types of <strong><em>environmental measurements</em></strong>. Select one or multiple characteristic groups. <br>Parentheses after each characteristic group represent which database(s) it is represented in.</center>';}
    static get characteristicsTooltip() { return '<center>Identifies types of <strong><em>environmental measurements</em></strong>. Select one or multiple characteristics. <br>Parentheses after each characteristic represent which database(s) it is represented in. The <br>names are derived from the <a href="http://iaspub.epa.gov/sor_internet/registry/substreg/home/overview/home.do">USEPA Substance Registry System (SRS)</a>. USGS uses <br>parameter codes for the same purpose and has <a href="http://www.waterqualitydata.us/public_srsnames.jsp">associated most parameters to SRS names</a>.</center>';}
    static get projectIDTooltip() { return '<center>Uniquely identifies a <strong><em>data collection project</em></strong>. Select one or multiple project IDs. <br>Parentheses after each project ID represent which database it is represented in.</center>';}
    static get paramCodeTooltip() { return '<center>Identifies a characteristic using <a href="https://nwis.waterdata.usgs.gov/usa/nwis/pmcodes"></em></em><strong><em>NWIS codes</em></strong></a>. Select one or multiple parameter <br>codes. Specifying a parameter code will limit the query to <strong><em>NWIS only</em></strong>.</center>';}
    static get minimumResultsTooltip() { return '<center>Returns only sites where at least a minimum number of <strong><em>results</em></strong> <br>have been reported. Select a value; the default is <strong>1</strong>.</center>';}
    static get bioSamplingTooltip() { return '<center>Filter by parameters specific to <strong><em>biological <br>organisms</em></strong>: assemblage and taxonomic name.</center>';}
    static get assemblageTooltip() { return '<center>An association of <strong><em>interacting populations</em></strong> of organisms in a given water body. <br><em>Example:</em> macroinvertabrates and fish/nekton.</center>';}
    static get taxNameTooltip() { return '<center><strong><em>Genus name, species name</em></strong> in binomial nomenclature. <br><em>Example:</em> for shovelnose strugeon, <em>Scaphirhyncus platorynchus</em>.</center>';}
    static get showAGOLTooltip() { return '<center>The Water Quality Portal (WQP) Web Services conform to the format defined in the below referenced XML schema.</center>';}
    static get sortDataTooltip() { return '<center><strong><em>Sorts data</em></strong> by <em>organization</em>, <em>monitoringLocationID</em>, and <em>activityID</em>. Sorting <strong>increases</strong> response time. <br>If you are manually sorting, set <strong>sorted=no</strong>. The sorted document is delivered in the WQX standard.</center>';}
    static get dateRangeTooltip() { return '<center><strong><em>Start</strong></em> and <strong><em>end dates</strong></em> to be used individually or together. <br></em>Dates must be entered in <em>MM-DD-YYYY</em> format.</center>'}
    static get databasesTooltip() { return '<center>Select one or multiple <strong><em>databases</strong></em> from which the data will <br>be retrieved. <strong>All</strong> databases are searched by default.</center>'}
    static get dataDownloadTooltip() { return '<center><strong><em>Water monitoring data</strong></em> is delivered in a format and nomenclature defined by the <a href="http://www.exchangenetwork.net/schema/WQX/2/WQX_DET_v2.1b.xls">WQX-<br>Outbound Schema</a>. <em>Metadata</em> on these formats is displayed in Tables 4-12 of the User Guide.</center>';}
    static get fileFormatTooltip() { return '<center>Choose a <strong><em>file format</strong></em> to download the result set.</center>';}
}