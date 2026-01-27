
<!-- md:swagger API|https://api.geosys-na.net/field-level-maps/v5/swagger/index.html -->

# Field Level Map APIs

EarthDaily Map APIs provide endpoints for retrieving **map image catalog** and **map generation**.

## APIs core concepts

| Term              | Definition |
|-------------------|------------|
| Map               | Resource created by a user from a set of fixed parameters, and from which several sub resources can fetched, and in various formats. Returned data is always fresh, recalculated if needed. |
| MapId             | Identifier for a stored map, for future access. |
| Generated Map     | Result data produced at a given time from fixed and dynamic parameters. |
| Fixed parameter   | Parameter provided by a user when creating a map. Example: image date, season field id, fertilizer dose, etc. |
| Dynamic parameter | Parameter whose value can change over time. Example: **•** Calculated parameters (best image from all images available for image date, season field id etc.) **•** Settings that can change (colormap profiles, etc.). |
| Image             | Image sub resource generated in various formats |
| Image format      | Format in which the map image resource (and just that) can be provided to a user |
| Legend            | Legend representing the colormap related to the representation of the map image, as a png file. |
| Dynamic Legend    | Legend related to the png representation of the map image. The number of classes is adapted according to the map variability |
| Fixed Legend      | Legend where the ranges and colors are previously specified for a given Map Product. |
| Thumbnail         | Smaller version of the png representation of the map image |

## APIs description

EarthDaily Map APIs are structured in map families that group different map types having common parameters types. 

For each map product, there are two different ways to generate a product:

- Request one Season Field or Geometry and a given image date:

  /field-level-maps/< version >/maps

- Request several Season Fields or geometries and/or several image dates:  
  
  /field-level-maps/< version >/map-sets
  
The API provides two different methods to request a map product : POST and GET. Requests in bulk mode are only available on POST method. Request on a geometry (and not an existing seasonfield) are only available on POST method.

In addition, to make easier the UI integration, the Map APIs provides shortcut endpoints with direct GET links. Taking by example the Base Reference Map Products swagger technical documentation:

![Intro](https://github.com/earthdaily/Images/blob/e07e71ed627e000d5ae9ee704261cfabfb2426f0/FLM/Swagger_shortcuts.png?raw=true)

### Base Route Pattern
EarthDaily Map APIs are using the following url patterns:

```json
`/season-fields/{SeasonFieldId}/coverage/{ImageDate}/{map-type-family}/{map-type}/{mandatoryParamName1}/{mandatoryParamValue1}/{mandatoryParamName2}/{mandatoryParamValue2}`
```

**Optional Parameters:** `?{optionalParamName1}={optionalParamValue1}&{optionalParamName2}={optionalParamValue2}`

You will find map description for each map types [here](./Map-types.md).

### Map Management APIs

| Method | Route | Description | Request Body | Response |
|--------|-------|-------------|--------------|----------|
| POST | `/map-sets/{map-type-family}/{map-type}` | Returns list of maps created by the user. For performance concerns, response doesn't contain any calculated data, only parameters and links to other endpoints that will calculate data. Maps are grouped following business rules to provide common legend. | JSON body with list of map parameters appropriate to the map type. | **JSON map details with:**<br>• Season field or geometry info<br>• [Optional] Maps Direct Links (legend, world file, thumbnail, images in various formats) |
| POST | `/maps/{map-type-family}/{map-type}` | Create one new map for specific parameters. | JSON body with map parameters appropriate to the map type. | **JSON maps list with:**<br>• Season field or geometry info<br>• [Optional] Map Direct Links (legend, world file, thumbnail, images in various formats) |

#### Map Shortcut APIs

Map Shortcut APIs should be used for simple map creation and access, as well as access to sub resources, with direct GET links.

Some Map Shortcut APIs return media files that can be directly displayed in a user interface by example. Please note that GEOTIFF and SHAPE formats are returned in ZIP file.

Direct map Shortcut APIs require authentication and URL never change because it’s generated with the request parameters.

Please note that the APIs that generate JSON responses for several season fields and/or several image dates can’t generate shortcuts for maps requiring complicated parameters because they can’t be set from request parameters.

Please also note that shortcut can only be used when working at seasonfield level.

| Method | Endpoint Suffix | Description | Response |
|--------|----------------|-------------|----------|
| GET | `/image.{format}` | Shortcut to the map image.<br>**Supported formats:**<br>• `png`<br>• `tiff.zip`<br>• `shp.zip` | Image binary data in requested format |
| GET | `/{resource}.png` | Shortcut to map resources.<br>**Supported resources:**<br>• `legend`<br>• `thumbnail` | Image resource binary data in PNG format |
| GET | `/worldfile` | Shortcut to the map world file data. | JSON information of the map world file |

### Optional parameters

#### MinZoneSize
This parameter defines the minimum size of the polygon generated. In case of a multipolygon, it’s applied on every polygon which is part of the multipolygon. This is expressed in user's field surface unit.

Sample request:

```
.../base-reference-map/INSEASON_NDVI?Zoning=True&ZoneCount=X&MinZoneSize=0.00001
```
<img width="800" height="200" src="https://github.com/GEOSYS/Images/blob/6888f4b5a4d73ddf71b0debcacff324d80baa80f/FLM/minzonesize.png?raw=true">


#### UseColorMapForZoning

This parameter is used to make the zoned map to look like a non zoned map or make them close enough on a display feel. ZoneCount cannot be used when UseColorMapForZoning is true.


!!! note "HOW TO USE FILTER MAPS.TYPE ON A COVERAGE?"

    The Coverage APIs allows to do a spatial query, based on a field boundary, a crop and a sowing date of imagery database. The results of the query will be an image catalog.
    By default, results include all the maps types and it can be useful to filter results by maps types.

      1- Example with one value: “INSEASON_NDVI”:

        https://<host>/field-level-maps/v5/season-fields/{SeasonFieldId}/catalog-imagery?Maps.Type=INSEASON_NDVI

      2- Example with multiple values: “INSEASON_NDVI” and “INSEASON_EVI”:

        https://<host>/field-level-maps/v5/season-fields/{SeasonFieldId}/catalog-imagery?Maps.Type=$in:INSEASON_NDVI|INSEASON_EVI

## API list

<swagger-ui src="https://api.geosys-na.net/field-level-maps/v5/swagger/v1/swagger.json"/>

## API response 

### Legend object 
Map response, except color compositon, includes a legend object that contains all information to create the legend on the UI. The legend object is a set of meta data including:
- Descriptive statistics derived from reflectance values used to generate the map
- Ranges are index classes used to generate the map including:
     - Color RGB codes
     - Number of pixel in the class
     - Minimum index value of the class
     - Maximum index value of the class

<br>
Here is an example of the legend object:

```json
   "legend": {
        "stat": {
            "max": 0.557,
            "mean": 0.1802,
            "min": 0.0233
        },
        "ranges": [
            {
                "color": {
                    "r": 138,
                    "g": 0,
                    "b": 0
                },
                "numberOfPixels": 64647,
                "maxValue": 0.25,
                "minValue": 0.0,
                "area": 84.93,
                "value": null
            },
            {
                "color": {
                    "r": 165,
                    "g": 0,
                    "b": 0
                },
                "numberOfPixels": 326,
                "maxValue": 0.3,
                "minValue": 0.25,
                "area": 0.4283,
                "value": null
            },
            {
                "color": {
                    "r": 190,
                    "g": 0,
                    "b": 0
                },
                "numberOfPixels": 257,
                "maxValue": 0.35,
                "minValue": 0.3,
                "area": 0.3376,
                "value": null
            },
...
```

### Map legend type

#### Dynamic legend
The legend fits between the min and max thresholds and consists of 13 classes with similar ranges.

This is the default legend.

This option is available for a Map set to get one legend per field while requesting maps for several fields in a single request.

Here is the syntax to use it:
```
POST  /field-level-maps/v5/map-sets/base-reference-map/INSEASON_NDVI?legendType=Dynamic
```

#### Fixed legend
Fixed legend means that the legend adopted will be the same whatever map you select. Minimum and maximum values are specific to the selected vegetation index, and the legend is composed of 15 classes with similar intervals.

 - NDVI, EVI, GNDVI, CVIn: between 0 and 1
 - CVI : between 0 and 15
 - NDWI: between -0.5 and 0.5
 - S2REP: between 705 and 740
 - LAI: between 0 and 8

Minimum and maximum thresholds are defined for fixed legends to be consistent with an agronomic context. However, your map may contain values outside these ranges (if there is snow on your plot, you may obtain a negative NDVI, for example). In this case, the extreme values will be included in the maximum - or minimum, depending on the case - while keeping the same intermediate ranges to ensure comparable legends for all maps.

Here is the syntax to use it:
```
GET   /field-level-maps/v5/maps/base-reference-map/INSEASON_NDVI/legend.png?legendType=Fixed
POST  /field-level-maps/v5/season-fields/bgv7pb3/coverage/2020-09-06/base-reference-map/INSEASON_NDVI/image.png?legendType=Fixed'
```

#### Common legend
This option is available for a Map set to get one common legend for several maps as part of a mapset.

The legend lies between the minimum and maximum values of all the fields included, so all fields will have the same legend. This makes it possible to have a similar legend for the fields and to be able to compare them, but in a more refined way than by using a fixed legend, as we continue to exacerbate the variability of this batch of fields.

Here is the syntax to use it:
```
POST  /field-level-maps/v5/map-sets/base-reference-map/INSEASON_NDVI?legendType=Common
```


### Histogram object

Histogram per map can be provided by activating the query parameter *histogram* and defining the number of bins in the the histogram using the parameter *numberOfBins*

All map requests except ColorComposition and FieldBorder can activate these parameters.

Request samples: 

```
.../field-level-maps/v5/season-fields/15avg72/coverage/2020-04-26/base-reference-map/INSEASON_NDVI?histogram=true&numberOfBins=5
```
These requests provide an histogram by map, even in the case of requests with common legend.

The “area” result parameter is provided based on user's unit.

Response content extract:

 ```json
"histogram": {
        "max": 0.8592,
        "mean": 0.4222,
        "min": 0.1347,
        "items": [
            {
                "valueMin": 0.1347,
                "valueMax": 0.2796,
                "numberOfPixel": 3235,
                "area": 8.2592
            },
            {
                "valueMin": 0.2796,
                "valueMax": 0.4245,
                "numberOfPixel": 10912,
                "area": 27.8591
            },
            {
                "valueMin": 0.4245,
                "valueMax": 0.5694,
                "numberOfPixel": 7621,
                "area": 19.4569
            },
...
 ```

### Worldfile object 
Map response,  includes a [worldfile](https://en.wikipedia.org/wiki/World_file) object that contains all informations used to position the map wihtin a GIS tool. It contains the same information as the pgw file but it is available as part the standard map request avoiding to fetch the pgw file.

The Woldfile object is a set of meta data including:
- A: pixel size in the x-direction in map units/pixel
- D: rotation about y-axis
- B: rotation about x-axis
- E: pixel size in the y-direction in map units, almost always negative[3]
- C: x-coordinate of the center of the upper left pixel
- 6: F: y-coordinate of the center of the upper left pixel


Response content extract:

 ```json
"worldFile": {
        "a": 2.81914906324328E-05,
        "d": 0.0,
        "b": 0.0,
        "e": -2.2805242098972E-05,
        "c": -97.7007439677583,
        "f": 37.147800314964
    },
 ```

### Mapsize object 
Map response,  includes a mapsize object that contains the size of the map as an image. 

The Mapsize object is a set of meta data including:
- Width of the map in pixel
- Height of the map in pixel

Response content extract:

 ```
 "mapSize": {
        "width": 298,
        "height": 330
    },
 ```

### Bbox object 
Map response,  includes a bounding box object (Bbox) that contains coordinate of the top left point and the bottom right pixel. 

<img width="300" height="200" src="https://github.com/GEOSYS/Images/blob/6888f4b5a4d73ddf71b0debcacff324d80baa80f/FLM/Bbox.png?raw=true">

The Bbox object is a set of meta data including:
- X Min coordinates of the map
- Y Min coordinates of the map
- X Max coordinates of the map
- Y Max coordinates of the map

Response content extract:

 ```json
     "bBox": {
        "xMin": -97.700758063503571,
        "xMax": -97.6923569992951,
        "yMin": 37.140285987692359,
        "yMax": 37.147811717585022
    }
 ```
 
## Zones object

Zoning capability allows to create a zoned map based off any “non-zoned” map (NDVI, GNDVI EVI, Yield Variability Map, Yield Goal Map, Organic Matter Variability Map, Elevation...) and the number of zones. 

To create a zoned map just add to paramter on the map request: 
```
.../base-reference-map/INSEASON_NDVI?Zoning=True&ZoneCount=X
```
With X being the number of zone (min=2 ans max=25)

Response content extract

```json
 "zones": [
        {
            "id": 1,
            "stats": {
                "mean": 2.7800202369689943E-05,
                "max": 3.3000001311302184E-05,
                "min": 2.3000000417232512E-05,
                "area": 44.852454533598689,
                "std": null
            },
            "segments": [
                {
                    "id": 1,
                    "geometry": "POLYGON ((-97.69807866 37.1471575, -97.69785789 37.14714076, -97.69782426 37.14712313, -97.69780325 37.14709392, -97.6978006 37.14695362, -97.69777389 37.14693001, -97.69765168 37.14690398, -97.69750948 37.14691731, -97.69731486 37.14698376, -97.69713908 37.14699963, -97.69612131 37.14693879, -97.69603638 37.14696739, -97.69598964 37.14703375, -97.6959577 37.14733491, -97.69581488 37.14738703, -97.6954727 37.14742055, -97.69489672 37.14744214, -97.69335049 37.14746869, -97.692777 37.14745955, -97.69261606 37.14742859, -97.69253683 37.14062335, -97.69265756 37.14049503, -97.69778835 37.14041483, -97.69817065 37.14059127, -97.69839198 37.14046295, -97.70048454 37.14044691, -97.70066562 37.14062335, -97.69927729 37.14227539, -97.69935777 37.14233954, -97.70004188 37.14248389, -97.70008212 37.14359058, -97.69863342 37.14495386, -97.69867367 37.14554728, -97.69855626 37.14578125, -97.69851292 37.14576195, -97.69849375 37.1457709, -97.69851278 37.1458252, -97.69852806 37.14583745, -97.6985127 37.14586805, -97.69842046 37.1458838, -97.69832553 37.14581865, -97.6982232 37.1457991, -97.6981616 37.14583425, -97.69813575 37.14588277, -97.69811653 37.14603605, -97.6981417 37.14618488, -97.698192 37.146234, -97.69807866 37.1471575), (-97.69480625 37.14559199, -97.69483103 37.14556605, -97.69487535 37.14554746, -97.69523585 37.1454129, -97.6953147 37.14531882, -97.69537431 37.14529477, -97.69541062 37.14530228, -97.69557838 37.14543579, -97.69565001 37.14545229, -97.69571387 37.14542818, -97.69570552 37.14526647, -97.69562956 37.14523036, -97.69491064 37.14519421, -97.69472566 37.14519146, -97.69466048 37.14522497, -97.69460604 37.14532314, -97.69475016 37.14556049, -97.69480625 37.14559199), (-97.69332403 37.1473105, -97.69328929 37.14728784, -97.69323981 37.14728812, -97.69323876 37.14730127, -97.69332403 37.1473105), (-97.6929647 37.14609323, -97.69297601 37.14602652, -97.69298776 37.14593343, -97.69296866 37.14551326, -97.69292182 37.1454541, -97.69285988 37.14543962, -97.69280167 37.14546711, -97.69278408 37.1455012, -97.6927794 37.14569613, -97.69286838 37.14604427, -97.69290283 37.14608116, -97.6929647 37.14609323), (-97.69431217 37.14537718, -97.69432196 37.14534572, -97.69434113 37.14531711, -97.69437201 37.14522483, -97.69432352 37.1451905, -97.69424515 37.14519406, -97.69411108 37.14526162, -97.69411471 37.14527887, -97.69421582 37.14535028, -97.69431217 37.14537718), (-97.69714187 37.14093752, -97.69715326 37.14088549, -97.69716518 37.14084873, -97.69716047 37.14081821, -97.69713681 37.140798, -97.69709945 37.14079122, -97.69701432 37.14081635, -97.69699265 37.14084742, -97.69699028 37.1408788, -97.69700815 37.14090622, -97.69705077 37.1409272, -97.69714187 37.14093752))",
                    "area": 448524.54533598688,
                    "stats": {
                        "mean": 2.7800202369689943E-05,
                        "max": 3.3000001311302184E-05,
                        "min": 2.3000000417232512E-05,
                        "area": 44.852454533598689,
                        "std": null
                    }
                }
            ]
        },
        {
            "id": 2,
            "stats": {
                "mean": 3.9214277267456052E-05,
                "max": 5.5000001192092894E-05,
                "min": 3.4000000357627867E-05,
                "area": 2.1462941027780329,
                "std": null
            },
            "segments": [
                {
                    "id": 2,
                    "geometry": "MULTIPOLYGON (((-97.6929647 37.14609323, -97.69290283 37.14608116, -97.69286838 37.14604427, -97.6927794 37.14569613, -97.69278408 37.1455012, -97.69280167 37.14546711, -97.69285988 37.14543962, -97.69292182 37.1454541, -97.69296866 37.14551326, -97.69298776 37.14593343, -97.69297601 37.14602652, -97.6929647 37.14609323)), ((-97.69451433 37.14765651, -97.69449116 37.14762271, -97.69429061 37.14757929, -97.69321844 37.14758133, -97.69279903 37.14760645, -97.69273684 37.14762335, -97.69261731 37.14753601, -97.69261606 37.14742859, -97.692777 37.14745955, -97.69335049 37.14746869, -97.69489672 37.14744214, -97.6954727 37.14742055, -97.69581488 37.14738703, -97.6959577 37.14733491, -97.69598964 37.14703375, -97.69603638 37.14696739, -97.69612131 37.14693879, -97.69713908 37.14699963, -97.69731486 37.14698376, -97.69750948 37.14691731, -97.69765168 37.14690398, -97.69777389 37.14693001, -97.6978006 37.14695362, -97.69780325 37.14709392, -97.69782426 37.14712313, -97.69785789 37.14714076, -97.69807866 37.1471575, -97.69804992 37.14739167, -97.69760727 37.14755205, -97.6965283 37.14758849, -97.69653207 37.14757098, -97.69643318 37.14752426, -97.69628686 37.14751341, -97.69620594 37.147531, -97.69614527 37.14756186, -97.69610413 37.1476008, -97.69610291 37.14760286, -97.69451433 37.14765651)), ((-97.69332403 37.1473105, -97.69323876 37.14730127, -97.69323981 37.14728812, -97.69328929 37.14728784, -97.69332403 37.1473105)), ((-97.698192 37.146234, -97.6981417 37.14618488, -97.69811653 37.14603605, -97.69813575 37.14588277, -97.6981616 37.14583425, -97.6982232 37.1457991, -97.69832553 37.14581865, -97.69842046 37.1458838, -97.6
```

For example based on an NDVI map here are example of zoned maps.
<img width="800" height="200" src="https://github.com/GEOSYS/Images/blob/6888f4b5a4d73ddf71b0debcacff324d80baa80f/FLM/Zoned%20map.png?raw=true">

The response contains for each zone created:
- Geometry WKT of the zone (this is most of the time a multipolygon)
- Area of the zone
- Descriptive statistics of the index used to create zones (min, max, mean, standard deviation)

Zoned map are available in several format: png, Tiff, KML, shapefile

Additionnal parameters allow to adapt the segmentation process.


--8<-- "snippets/contact-footer.md"