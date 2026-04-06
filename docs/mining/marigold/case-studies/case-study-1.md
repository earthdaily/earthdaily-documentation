---
title: "Case Study: Cuprite - Low Sulphidation Epithermal"
description: "Step-by-step guide to generating and interpreting mineral mapping products for low sulphidation epithermal deposits using Marigold, demonstrated at the Cuprite spectral reference site in Nevada."
keywords:
  - Cuprite
  - low sulphidation epithermal
  - mineral mapping
  - bare earth composite
  - spectral analysis
  - alteration minerals
  - Marigold case study
---

# Case Study: Cuprite (low sulphidation epithermal)

This case study provides a step-by-step guide covering how to generate and
interpret our recommended mapping products for low sulphidation epithermal
deposits. You can follow along by walking through the case study, or load the
linked Marigold project file to automatically load the products into Marigold.

+----------------------------------+----------------------------------+ |
**Deposit type** | Low Sulphidation Epithermal |
+==================================+==================================+ |
**Location** | Cuprite, Nevada, USA |
+----------------------------------+----------------------------------+ |
\------------------------------ | ------------------------------ |
+----------------------------------+----------------------------------+ |
**Commodity** | Au, Cu |
+----------------------------------+----------------------------------+ |
\------------------------------ | ------------------------------ |
+----------------------------------+----------------------------------+ |
**Marigold file** | `Get some sort of shared demo file going` |
+----------------------------------+----------------------------------+

## Background

### Spectral reference site

**Lat/lon** 37.542628, -117.196650

---

**Zoom** 13

### Deposit description

This desert site is well known for its excellent exposure, and diverse suite of
exposed alteration minerals including advanced argillic alteration (alunite), an
extended suite of argillic alteration, as well as a type-locality of
ammonium-rich clays (buddingtonite). There is little vegetation on-site except
for some lichen. It is characterized as a low sulphidation quartz-adularia hot
spring type epithermal deposit, which was overprinted by late-stage steam-heated
advanced argillic alteration. Mapped alteration includes Fe-oxides, hydrothermal
minerals, many AlOH-species such as clays and micas, as well as sulfates,
carbonates and silicates and siliceous alteration (Swayze et al., 2014).

### Mining history

This location was intensively prospected for sulphur and mercury, and mined for
silicates, but never for metal content. No significant precious metal
mineralization has been found. It has been extensively explored and mapped using
remote sensing techniques, and is used as a spectral reference site for many
sensors for geological remote sensing / mineral mapping.

### Characteristics of Low Sulphidation (LS) Epithermal Systems

Epithermal (gold) systems have characteristic mineral alteration assemblages,
although there are of course distinctive spectral characteristics associated
with each deposit. The mineral assemblages typically define zonation in the
alteration system, so being able to recognize the mineral groupings, and this
zonation in surface mapping can be key to targeting the orebody, proximal to
distal relationships to mineralization and of course help to guide future
exploration decisions. Low sulphidation systems like Cuprite typically have
alteration zones dominated by the argillic clays, formed from near-neutral
hydrothermal fluids. The clay assemblage and zonation largely reflects
decreasing temperatures outward from fluid conduits, from illitic clays near the
centre of the system and outward through illite-smectite to smectite. Peripheral
to the argillic alteration is a propylitic alteration zone, which may have a
sub-propylitic zone. This particular deposit also exhibits a late-stage advanced
argillic overprinting associated with a steam-heated event (GMEX, vol 4,
Epithermal Alteration Systems).

### Detailed zonation

+----------------------------------+----------------------------------+ |
**Advanced argillic** | alunite (K, Na-K, & Na), | | | kaolinite, dickite, | | |
buddingtonite |
+==================================+==================================+ |
**Central & mineralized zone** | quartz-adularia assemblage - may | | | be
quartz, adularia, opal, | | | chalcedony |
+----------------------------------+----------------------------------+ |
\------------------------------ | ------------------------------ |
+----------------------------------+----------------------------------+ |
**Argillic alteration** | AlOH clays - mainly illite, | | | illite-smectite,
smectite with | | | carbonate |
+----------------------------------+----------------------------------+ |
\------------------------------ | ------------------------------ |
+----------------------------------+----------------------------------+ |
**Propylitic alteration** | chlorite, epidote, carbonate |
+----------------------------------+----------------------------------+

## Processing guide

Now we'll use Marigold to generate and interpret a series of products using the
Fused Bare Earth Composite over Cuprite. Before that, a couple notes.

Each of the products generated here are covered in the Multispectral Mineral
Processing Reference worksheet. The worksheet identifies how to compute the
product using any of the different commonly used geological remote sensing
datasets and what the products were designed to highlight. It's a useful
reference to check out.

Also note that Cuprite is a spectral reference site, we're reviewing a few
additional products in an effort to demonstrate that mineral mapping using
multispectral data like Sentinel-2 & ASTER is truly mapping mineral groups,
rather than mineral species. The ground truth maps illustrate that the minerals
are very intermixed here. When a product is designed to highlight the
characteristics of a specific mineral or mineral group (i.e. Mica_clay), it
doesn't mean that the product will preferentially map that mineral. In fact it
will generally map most of the AlOH ASTER band 6 minerals that generate an
absorption feature at that band. This is why multispectral mineral mapping need
validation to confirm the mapping results. In addition to reviewing the typical
patterns observed for this deposit type, we'll also review their limitations.

Ok, let's get to it!

### Product 1: True color composite

![image](images/case-study1_image1.jpg)

This product provides an excellent overview of the site being targeted in a band
combination that is generally used by more exploration teams as a basemap. Also
note that Ferric Fe-rich gossans or areas of hematite and/or goethite iron
oxides may be visible as reddish-brown cover materials (as is shown below).

- Add the Fused Bare Earth Composite to the map, and use the Settings to map the
  red, green, and blue bands to RGB.
- Apply a linear 2% stretch by clicking the magic wand.

### Product 2: False color composite

![image](images/case-study1_image2.jpg)

## Product 3: AST(6,4,1)eq as (R,G,B)

![image](images/case-study1_image3.jpg) Product 4: AST(6,4,1)eq_dc as (R,G,B)

---

![image](images/case-study1_image4.jpg) Product 5: AST(9,5,4)eq as (R,G,B)

---

![image](images/case-study1_image5.jpg) Product 6: Fused BEC - FerricOX_comp (L)
with linear 2% stretch; (R) thresholded results

---

![image](images/case-study1_image6a.jpg)
![image](images/case-study1_image6b.jpg) Product 7: Fused BEC - ALI_index (L)
with linear 2% stretch; (R) thresholded results\
![image](images/case-study1_image6a.jpg)\
![image](images/case-study1_image6b.jpg)

---

Product 8: Fused BEC - AlOH_b5_index. (L) with linear 2% stretch; (R)
thresholded results\
![image](images/case-study1_image7a.jpg)\
![image](images/case-study1_image7b.jpg)

---

Product 9: Fused BEC - Hewson_kaol (L) with linear 2% stretch; (R) thresholded
results\
![image](images/case-study1_image8a.jpg)\
![image](images/case-study1_image8b.jpg)

---

Product 10: Fused BEC - KaolGrp_index (L) with linear 2% stretch; (R)
thresholded results\
![image](images/case-study1_image9a.jpg)\
![image](images/case-study1_image9b.jpg)

---

Product 11: Fused BEC - AlOH_b6_index (L) with linear 2% stretch; (R)
thresholded results\
![image](images/case-study1_image10a.jpg)\
![image](images/case-study1_image10b.jpg)

---

Product 12: Fused BEC - Mica_clay (L) with linear 2% stretch; (R) thresholded
results\
![image](images/case-study1_image11a.jpg)\
![image](images/case-study1_image11b.jpg)

---

Product 13: Fused BEC - KLI_index (L) with linear 2% stretch; (R) thresholded
results\
![image](images/case-study1_image12a.jpg)\
![image](images/case-study1_image12b.jpg)

---

Product 14: Fused BEC - MgOH_Grp_comp (L) with linear 2% stretch; (R)
thresholded results\
![image](images/case-study1_image13a.jpg)\
![image](images/case-study1_image13b.jpg)

---

Product 15: Fused BEC - MgOH_b8_index (L) with linear 2% stretch; (R)
thresholded results\
![image](images/case-study1_image14a.jpg)\
![image](images/case-study1_image14b.jpg)

---

Product 16: Fused BEC - MgOH_grpCont (L) with linear 2% stretch; (R) thresholded
results\
![image](images/case-study1_image15a.jpg)\
![image](images/case-study1_image15b.jpg)

---

Product 17: Fused BEC - WV3_carb_index (L) with linear 2% stretch; (R)
thresholded results\
![image](images/case-study1_image16a.jpg)\
![image](images/case-study1_image16b.jpg)

---

Product 18: Fused BEC - FeOH_b7_index (L) with linear 2% stretch; (R)
thresholded results\
![image](images/case-study1_image17a.jpg)\
![image](images/case-study1_image17b.jpg)

---

Product 19: Emissivity - Silica_index (SI) (L) with linear 2% stretch; (R)
thresholded results\
![image](images/case-study1_image18a.jpg)\
![image](images/case-study1_image18b.jpg)

---

Product 20: Band Ratio - (AST_b5/SEN_b8) - (swir2/nir)\
![image](images/case-study1_image19.jpg)

---

Product 21: Band Ratio - (AST_b4/SEN_b4) - (swir1/red)\
![image](images/case-study1_image20.jpg)

---

Product 22: Band Ratio - (AST_b4/AST_b7) - (swir1/red)\
![image](images/case-study1_image21.jpg)

---

Product 23: Band Ratio - (AST_b4/Sen_S8) - (swir1/red)\
![image](images/case-study1_image22.jpg)

---

Product 24: TRatio12 - (AlOH_B6_Index, AST_b5/SEN_b8, FeOH_b7_index)\
![image](images/case-study1_image23.jpg)

---

Product 25: Fused BEC - TRatio13 with linear 2% stretch\
![image](images/case-study1_image24.jpg)

---

Product 26: Fused BEC - TRatio22 (ALI, KLI, FerricOX) with linear 2% stretch\
![image](images/case-study1_image25.jpg)

---

Product 27: Fused BEC - TRatio3 with linear 2% stretch\
![image](images/case-study1_image26.jpg)

---

Product 28: Fused BEC - PCA(v-s)\_123 with linear 2% stretch\
![image](images/case-study1_image27.jpg)

---

Product 29: Fused BEC - MNF(v-s)\_123 with linear 2% stretch\
![image](images/case-study1_image28.jpg)

---

Product 30: Fused BEC - Alunite Hill - SAM Spectral Similarity (L) with linear
2% stretch; (R) thresholded search results displayed with a magma colour table
over the Cuprite AOI\
![image](images/case-study1_image29a.jpg)\
![image](images/case-study1_image29b.jpg)

## Reference Ground Truthing Documentation and Maps for Cuprite

![image](images/case-study1_image31.jpg)

![image](images/case-study1_image32.jpg)

![image](images/case-study1_image33.jpg)

![image](images/case-study1_image34.jpg)

--8<-- "snippets/contact-footer.md"
