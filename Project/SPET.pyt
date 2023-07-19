import arcpy

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Solar Power Estimation Tools (SPET)"
        self.alias = "toolbox"

        # List of tool classes associated with this toolbox
        self.tools = [Solar_Radiation_Estimation, Suitable_Rooftop]

     
class Solar_Radiation_Estimation(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Solar Radiation Estimation"
        self.description = "A Solar Power Estimation Tool"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arcpy.Parameter(displayName = "Input raster", name = "Raster input", datatype = "DERasterDataset", parameterType = "Required", direction = "Input")
        param1 = arcpy.Parameter(displayName = "Hour interval", name = "time_intrv", datatype = "GPLong", parameterType = "Required", direction = "Input")
        param2 = arcpy.Parameter(displayName = "Calculation directions", name = "cal dir", datatype = "GPLong", parameterType = "Required", direction = "Input")
        param3 = arcpy.Parameter(displayName = "Local surface type", name = "surface type", datatype = "GPString", parameterType = "Required", direction = "Input")
        lst_list = ['QUADRATIC', 'BIQUADRATIC']
        param3.filter.type = "ValueList"
        param3.filter.list = lst_list
        param4 = arcpy.Parameter(displayName = "Neighborhood distance", name = "n_dist", datatype = "GPLinearUnit", parameterType = "Required", direction = "Input")
        param5 = arcpy.Parameter(displayName = "Slope measurement type", name = "out_slope", datatype = "GPString", parameterType = "Required", direction = "Input")
        osm_list = ['DEGREE', 'PERCENT_RISE']
        param5.filter.type = "ValueList"
        param5.filter.list = osm_list
        param6 = arcpy.Parameter(displayName = "Steep/High slope threshold", name = "StpSlopeThrhld", datatype = "GPLong", parameterType = "Required", direction = "Input")
        param6.filter.type = "Range"
        param6.filter.list = [0, 90]
        param7 = arcpy.Parameter(displayName = "Minimum solar radiation", name = "MinSolRad", datatype = "GPLong", parameterType = "Required", direction = "Input")
        param8 = arcpy.Parameter(displayName = "Flat/Low slope threshold", name = "FltSlopeThrhld", datatype = "GPLong", parameterType = "Required", direction = "Input")
        param8.filter.type = "Range"
        param8.filter.list = [0, 90]
        param9 = arcpy.Parameter(displayName = "Minimum north-facing slope", name = "MinNFSlopeThrhld", datatype = "GPLong", parameterType = "Required", direction = "Input")
        param9.filter.type = "Range"
        param9.filter.list = [0, 360]
        param10 = arcpy.Parameter(displayName = "Maximum north-facing slope", name = "MaxNFSlopeThrhld", datatype = "GPLong", parameterType = "Required", direction = "Input")
        param10.filter.type = "Range"
        param10.filter.list = [0, 360]
        param11 = arcpy.Parameter(displayName = "Input feature layer", name = "inputFC", datatype = "DEFeatureClass", parameterType = "Required", direction = "Input")
        param12 = arcpy.Parameter(displayName = "Zonal Statistics field", name = "Zonefld", datatype = "Field", parameterType = "Required", direction = "Input")
        param12.parameterDependencies = [param11.name]
        param13 = arcpy.Parameter(displayName = "Ouput location", name = "OutputFolder", datatype = "DEWorkspace", parameterType = "Required", direction = "Input")
        param14 = arcpy.Parameter(displayName = "Table name", name = "ZSName", datatype = "GPTableView", parameterType = "Required", direction = "Output")
        param15 = arcpy.Parameter(displayName = "New feature layer name", name = "NBFeature", datatype = "DEFeatureClass", parameterType = "Required", direction = "Output")
        params = [param0, param1, param2, param3, param4, param5, param6, param7, param8, param9, param10, param11, param12, param13, param14, param15]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        #from arcpy.sa import
        arcpy.CheckOutExtension("Spatial")
        arcpy.env.workspace = parameters[11].ValueAsText
        arcpy.env.overwriteOutput = True
        
        
        # Check out any necessary licenses.
        arcpy.CheckOutExtension("spatial")
        arcpy.CheckOutExtension("ImageAnalyst")
        arcpy.CheckOutExtension("3D")
        arcpy.CheckOutExtension("ImageExt")
        
        # Set Geoprocessing environments
        #arcpy.env.snapRaster = "C:\\Users\\Samuel\\Documents\\GEOG_592\\Lab5\\SuitabilityModeling\\Data.gdb\\Elevation"
        #arcpy.env.extent = "439952.113762345 200181.284694512 513122.113762345 253671.284694512"
        #arcpy.env.cellSize = "30"
        #arcpy.env.mask = "C:\\Users\\Samuel\\Documents\\GEOG_592\\Lab5\\SuitabilityModeling\\Data.gdb\\Elevation"
        
        DSM = arcpy.Raster(parameters[0].ValueAsText)
                
        # Process: Area Solar Radiation (Area Solar Radiation) (sa)
        Solar_Rad_Whm2 = "Solar_Rad_Whm2"
        Area_Solar_Radiation = Solar_Rad_Whm2
        Output_direct_radiation_raster = ""
        Output_diffuse_radiation_raster = ""
        Output_direct_duration_raster = ""
        Solar_Rad_Whm2 = arcpy.sa.AreaSolarRadiation(in_surface_raster=DSM, latitude=38.92157611011734, sky_size=200, 
                                                         time_configuration="WholeYear 2023", day_interval=14, 
                                                         hour_interval=12, each_interval="NOINTERVAL", z_factor=1, 
                                                         slope_aspect_input_type="FROM_DEM", calculation_directions=parameters[2].ValueAsText, 
                                                         zenith_divisions=8, azimuth_divisions=8, diffuse_model_type="UNIFORM_SKY", 
                                                         diffuse_proportion=0.3, transmittivity=0.5, 
                                                         out_direct_radiation_raster=Output_direct_radiation_raster, 
                                                         out_diffuse_radiation_raster=Output_diffuse_radiation_raster, 
                                                         out_direct_duration_raster=Output_direct_duration_raster)
        Solar_Rad_Whm2.save(Area_Solar_Radiation)


        # Process: Surface Parameters (2) (Surface Parameters) (sa)
        Aspect_DSM = "Aspect_DSM"
        Surface_Parameters_2_ = Aspect_DSM
        Aspect_DSM = arcpy.sa.SurfaceParameters(in_raster=DSM, parameter_type="ASPECT", local_surface_type=parameters[3].ValueAsText, 
                                                    neighborhood_distance=parameters[4].ValueAsText, use_adaptive_neighborhood="FIXED_NEIGHBORHOOD", 
                                                    z_unit="METER", output_slope_measurement=parameters[5].ValueAsText, project_geodesic_azimuths="GEODESIC_AZIMUTHS", 
                                                    use_equatorial_aspect="NORTH_POLE_ASPECT")
        Aspect_DSM.save(Surface_Parameters_2_)


        # Process: Surface Parameters (Surface Parameters) (sa)
        Slope_DSM = "Slope_DSM"
        Surface_Parameters = Slope_DSM
        Slope_DSM = arcpy.sa.SurfaceParameters(in_raster=DSM, parameter_type="SLOPE", local_surface_type=parameters[3].ValueAsText, 
                                                   neighborhood_distance=parameters[4].ValueAsText, use_adaptive_neighborhood="FIXED_NEIGHBORHOOD", 
                                                   z_unit="METER", output_slope_measurement=parameters[5].ValueAsText, project_geodesic_azimuths="GEODESIC_AZIMUTHS", 
                                                   use_equatorial_aspect="NORTH_POLE_ASPECT")
        Slope_DSM.save(Surface_Parameters)


        # Process: Raster Calculator (Raster Calculator) (ia)
        Solar_Rad = "Solar_Rad"
        Raster_Calculator = Solar_Rad
        Solar_Rad =  Solar_Rad_Whm2 /1000
        Solar_Rad.save(Raster_Calculator)


        # Process: Con (Con) (sa)
        Solar_Rad_slope = "Solar_Rad_slope"
        Con = Solar_Rad_slope
        Solar_Rad_slope = arcpy.sa.Con(in_conditional_raster=Slope_DSM, in_true_raster_or_constant=Solar_Rad, 
                                           in_false_raster_or_constant="", where_clause="VALUE <= "+str(parameters[6].ValueAsText))
        Solar_Rad_slope.save(Con)


        # Process: Con (2) (Con) (sa)
        Solar_Rad_slope_HS = "Solar_Rad_slope_HS"
        Con_2_ = Solar_Rad_slope_HS
        Solar_Rad_slope_HS = arcpy.sa.Con(in_conditional_raster=Solar_Rad_slope, in_true_raster_or_constant=Solar_Rad_slope, 
                                              in_false_raster_or_constant="", where_clause="VALUE >= "+str(parameters[7].ValueAsText))
        Solar_Rad_slope_HS.save(Con_2_)


        # Process: Con (3) (Con) (sa)
        Solar_Rad_Low_Slope = "Solar_Rad_Low_Slope"
        Con_3_ = Solar_Rad_Low_Slope
        Solar_Rad_Low_Slope = arcpy.sa.Con(in_conditional_raster=Slope_DSM, in_true_raster_or_constant=Solar_Rad_slope_HS, 
                                               in_false_raster_or_constant="", where_clause="VALUE <= "+str(parameters[8].ValueAsText))
        Solar_Rad_Low_Slope.save(Con_3_)


        # Process: Con (4) (Con) (sa)
        Solar_Rad_slope_HS_NN = "Solar_Rad_slope_HS_NN"
        Con_4_ = Solar_Rad_slope_HS_NN
        mini = str(parameters[9].ValueAsText)
        maxi = str(parameters[10].ValueAsText)
        Solar_Rad_slope_HS_NN = arcpy.sa.Con(in_conditional_raster=Aspect_DSM, in_true_raster_or_constant=Solar_Rad_slope_HS, 
                                             in_false_raster_or_constant=Solar_Rad_Low_Slope, 
                                             where_clause="VALUE > {} And VALUE < {}".format(mini, maxi))
        Solar_Rad_slope_HS_NN.save(Con_4_)

        # Process: Zonal Statistics as Table (Zonal Statistics as Table) (sa)
        #ZonalSt_Buildin1 = "C:\\Users\\Samuel\\Documents\\GEOG_592\\MiniProject\\GISC_Project.gdb\\ZonalSt_Buildin1"
        #ZonalSt_Buildin1 = "ZonalSt_Buildin1"
        arcpy.sa.ZonalStatisticsAsTable(in_zone_data=parameters[11].ValueAsText, zone_field=parameters[12].ValueAsText, in_value_raster=Solar_Rad_slope_HS_NN, 
                                        out_table=parameters[14].ValueAsText, ignore_nodata="DATA", statistics_type="MEAN", process_as_multidimensional="CURRENT_SLICE", 
                                        percentile_values=90, percentile_interpolation_type="AUTO_DETECT", circular_calculation="ARITHMETIC", circular_wrap_value=360)
        arcpy.TableToTable_conversion(in_rows=parameters[14].ValueAsText, out_path=parameters[13].ValueAsText, out_name="Zonal_Statistics_as_Table")

        # Process: Join Field (Join Field) (management)
        Building_feature = arcpy.management.JoinField(in_data=parameters[11].ValueAsText, in_field=parameters[12].ValueAsText, join_table=parameters[14].ValueAsText, 
                                                      join_field=parameters[12].ValueAsText, fields=["AREA", "MEAN"], fm_option="NOT_USE_FM", field_mapping="")[0]
        #parameters[13].ValueAsText = Building_feature
        arcpy.CopyFeatures_management(Building_feature, parameters[15].ValueAsText)

        arcpy.AddMessage("Condition raster created successfully")
        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return
    
        
class Suitable_Rooftop(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Suitable Building Calculation"
        self.description = "A Building rooftop power calculation Tool"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arcpy.Parameter(displayName = "Input feature layer", name = "inputFC", datatype = "DEFeatureClass", parameterType = "Required", direction = "Input")
        param1 = arcpy.Parameter(displayName = "Building Rooftop area threshold", name = "BRThrhld", datatype = "GPLong", parameterType = "Required", direction = "Input")
        param2 = arcpy.Parameter(displayName = "Selected rooftop layer name", name = "Suitable_ExportFeatures", datatype = "DEFeatureClass", parameterType = "Required", direction = "Output")
        param3 = arcpy.Parameter(displayName = "Field name 1", name = "fldName1", datatype = "GPString", parameterType = "Required", direction = "Input")
        param4 = arcpy.Parameter(displayName = "Field name 2", name = "fldName2", datatype = "GPString", parameterType = "Required", direction = "Input")
        param5 = arcpy.Parameter(displayName = "Ouput location", name = "OutputFolder", datatype = "DEWorkspace", parameterType = "Optional", direction = "Input")
        param6 = arcpy.Parameter(displayName = "Final feature layer name", name = "Suitable_Features", datatype = "DEFeatureClass", parameterType = "Required", direction = "Output")
        params = [param0, param1, param2, param3, param4, param5, param6]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        #from arcpy.sa import
        arcpy.CheckOutExtension("Spatial")
        #arcpy.env.workspace = "C:\\Users\\Samuel\\Documents\\GEOG_592\\MiniProject\\Solar_in_Glover.gdb"
        arcpy.env.workspace = parameters[4].ValueAsText
        arcpy.env.overwriteOutput = True
       
        # Check out any necessary licenses.
        arcpy.CheckOutExtension("spatial")
        arcpy.CheckOutExtension("ImageAnalyst")
        arcpy.CheckOutExtension("3D")
        arcpy.CheckOutExtension("ImageExt")        

        # Process: Select Layer By Attribute (Select Layer By Attribute) (management)
        Building_Footprints_3_, Count = arcpy.management.SelectLayerByAttribute(in_layer_or_view=parameters[0].ValueAsText, selection_type="NEW_SELECTION", 
                                                                                where_clause="AREA > "+str(parameters[1].ValueAsText), invert_where_clause="")
        # Process: Export Features (Export Features) (conversion)
        Suitable_ExportFeatures = "C:\\Users\\Samuel\\Documents\\GEOG_592\\MiniProject\\GISC_Project.gdb\\Suitable_ExportFeatures"
        arcpy.conversion.ExportFeatures(in_features=Building_Footprints_3_, out_features=parameters[2].ValueAsText, where_clause="", use_field_alias_as_name="NOT_USE_ALIAS", 
                                        sort_field=[])

        # Process: Add Field (Add Field) (management)
        Suitable_ExportFeatures_2_ = arcpy.management.AddField(in_table=parameters[2].ValueAsText, field_name=parameters[3].ValueAsText, field_type="DOUBLE", field_precision=2, 
                                                               field_scale=None, field_length=None, field_alias="", field_is_nullable="NULLABLE", 
                                                               field_is_required="NON_REQUIRED", field_domain="")[0]
        Suitable_ExportFeatures_2_ = arcpy.management.AddField(in_table=parameters[2].ValueAsText, field_name=parameters[4].ValueAsText, field_type="DOUBLE", field_precision=2, 
                                                               field_scale=None, field_length=None, field_alias="", field_is_nullable="NULLABLE", 
                                                               field_is_required="NON_REQUIRED", field_domain="")[0]

        # Process: Calculate Field (Calculate Field) (management)
        Suitable_ExportFeatures_3_ = arcpy.management.CalculateField(in_table=Suitable_ExportFeatures_2_, field=parameters[3].ValueAsText, expression="(!AREA! * !MEAN!) / 1000", 
                                                                     expression_type="PYTHON3", code_block="", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")[0]
        Suitable_ExportFeatures_3_ = arcpy.management.CalculateField(in_table=Suitable_ExportFeatures_2_, field=parameters[4].ValueAsText, expression="!"+parameters[3].ValueAsText+"! * 0.16 * 0.86", 
                                                                     expression_type="PYTHON3", code_block="", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")[0]
        arcpy.CopyFeatures_management(Suitable_ExportFeatures_3_, parameters[6].ValueAsText)

        arcpy.AddMessage("Suitable Building rooftop calculation successfully")
        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return