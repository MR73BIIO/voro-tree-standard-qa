<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.40.0" styleCategories="Symbology|Labeling|Fields">
  <renderer-v2 type="categorizedSymbol" attr="waga" symbollevels="0" enableorderby="0" forceraster="0">
    <categories>
      <category value="blad" symbol="0" label="błąd / Fehler / error" render="true"/>
      <category value="ostrzezenie" symbol="1" label="ostrzeżenie / Warnung / warning" render="true"/>
      <category value="informacja" symbol="2" label="informacja / Hinweis / note" render="true"/>
    </categories>
    <symbols>
      <symbol type="marker" name="0" alpha="1" clip_to_extent="1" force_rhr="0">
        <layer class="SimpleMarker" enabled="1" locked="0" pass="2">
          <Option type="Map">
            <Option type="QString" name="name" value="circle"/>
            <Option type="QString" name="color" value="178,58,46,255"/>
            <Option type="QString" name="outline_color" value="255,255,255,255"/>
            <Option type="QString" name="outline_width" value="0.6"/>
            <Option type="QString" name="size" value="4.6"/>
          </Option>
        </layer>
      </symbol>
      <symbol type="marker" name="1" alpha="1" clip_to_extent="1" force_rhr="0">
        <layer class="SimpleMarker" enabled="1" locked="0" pass="1">
          <Option type="Map">
            <Option type="QString" name="name" value="triangle"/>
            <Option type="QString" name="color" value="226,160,40,255"/>
            <Option type="QString" name="outline_color" value="80,50,0,255"/>
            <Option type="QString" name="outline_width" value="0.4"/>
            <Option type="QString" name="size" value="4.6"/>
          </Option>
        </layer>
      </symbol>
      <symbol type="marker" name="2" alpha="1" clip_to_extent="1" force_rhr="0">
        <layer class="SimpleMarker" enabled="1" locked="0" pass="0">
          <Option type="Map">
            <Option type="QString" name="name" value="square"/>
            <Option type="QString" name="color" value="59,106,143,255"/>
            <Option type="QString" name="outline_color" value="255,255,255,255"/>
            <Option type="QString" name="outline_width" value="0.4"/>
            <Option type="QString" name="size" value="3.6"/>
          </Option>
        </layer>
      </symbol>
    </symbols>
  </renderer-v2>
  <labeling type="simple">
    <settings calloutType="simple">
      <text-style fieldName="concat(&quot;nr&quot;, ' · ', &quot;regula&quot;)" isExpression="1" fontSize="8" textColor="30,30,30,255">
        <text-buffer bufferDraw="1" bufferSize="0.8" bufferColor="255,255,255,255"/>
      </text-style>
      <placement placement="0" dist="1.5"/>
      <rendering scaleVisibility="1" scaleMin="1" scaleMax="5000"/>
    </settings>
  </labeling>
  <mapTip enabled="1">&lt;b&gt;[% "nr" %] · [% "regula" %]&lt;/b&gt;&lt;br&gt;PL: [% "msg_pl" %]&lt;br&gt;DE: [% "msg_de" %]&lt;br&gt;EN: [% "msg_en" %]&lt;br&gt;&lt;i&gt;Standard 688/2025: [% "standard" %]&lt;/i&gt;</mapTip>
  <previewExpression>concat("nr", ' · ', "regula")</previewExpression>
</qgis>
