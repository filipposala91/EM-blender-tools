#    part of this library is a heavy modified version of the original code from: 
#    "name": "Super Grouper",
#    "author": "Paul Geraskin, Aleksey Juravlev, BA Community",

import bpy

from .functions import *
from bpy.props import *
from bpy.types import Operator
from bpy.types import Menu, Panel, UIList, PropertyGroup
from bpy.props import StringProperty, BoolProperty, IntProperty, CollectionProperty, BoolVectorProperty, PointerProperty
from bpy.app.handlers import persistent
from .epoch_manager import *
from .EM_list import *
from . import addon_updater_ops



#####################################################################
#US/USV Manager
class EM_ToolsPanel:
    bl_label = "US/USV Manager"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        #addon_updater_ops.check_for_update_background(context)
        layout = self.layout
        scene = context.scene
        em_settings = scene.em_settings
        obj = context.object
        #layout.alignment = 'LEFT'
        row = layout.row()

        if scene.em_list_index >= 0 and len(scene.em_list) > 0:
            row.template_list("EM_UL_List", "EM nodes", scene, "em_list", scene, "em_list_index")
            item = scene.em_list[scene.em_list_index]
            box = layout.box()
            row = box.row(align=True)
            #row.label(text="US/USV name, description:")
            #row = box.row()
            split = row.split()
            col = split.column()
            row.prop(item, "name", text="")
            split = row.split()
            col = split.column()
            op = col.operator("listitem.toobj", icon="PASTEDOWN", text='')
            op.list_type = "em_list"
            #row = layout.row()
            #row.label(text="Description:")
            row = box.row()
            #layout.alignment = 'LEFT'
            row.prop(item, "description", text="", slider=True, emboss=True)

            split = layout.split()
            if scene.em_list[scene.em_list_index].icon == 'RESTRICT_INSTANCED_OFF':
                col = split.column()
                op = col.operator("select.fromlistitem", text='', icon="MESH_CUBE")
                op.list_type = "em_list"
            else:
                col = split.column()
                col.label(text="", icon='MESH_CUBE') 
            if obj:
                if check_if_current_obj_has_brother_inlist(obj.name, "em_list"):
                    col = split.column(align=True)
                    op = col.operator("select.listitem", text='', icon="LONGDISPLAY")
                    op.list_type = "em_list"
                else:
                    col = split.column()
                    col.label(text="", icon='LONGDISPLAY')             
                    
            #split = layout.split()
            col = split.column(align=True)
            col.label(text="Sync:")

            col = split.column(align=True)
            col.prop(em_settings, "em_proxy_sync2", text='', icon="MESH_CUBE")

            col = split.column(align=True)
            col.prop(em_settings, "em_proxy_sync2_zoom", text='', icon="ZOOM_SELECTED")

            col = split.column(align=True)
            col.prop(em_settings, "em_proxy_sync", text='', icon="LONGDISPLAY")

            col = split.column(align=True)
            col.prop(scene, "paradata_streaming_mode", text='', icon="SHORTDISPLAY")

            if scene.em_settings.em_proxy_sync is True:
                if obj is not None:
                    if check_if_current_obj_has_brother_inlist(obj.name, "em_list"):
                            select_list_element_from_obj_proxy(obj, "em_list")
                    
            if scene.em_settings.em_proxy_sync2 is True:
                if scene.em_list[scene.em_list_index].icon == 'RESTRICT_INSTANCED_OFF':
                    list_item = scene.em_list[scene.em_list_index]
                    if obj is not None:
                        if list_item.name != obj.name:
                            select_3D_obj(list_item.name)
                            if scene.em_settings.em_proxy_sync2_zoom is True:
                                for area in bpy.context.screen.areas:
                                    if area.type == 'VIEW_3D':
                                        ctx = bpy.context.copy()
                                        ctx['area'] = area
                                        ctx['region'] = area.regions[-1]
                                        bpy.ops.view3d.view_selected(ctx)

            
        else:
            row.label(text="No US/USV here :-(")

class VIEW3D_PT_ToolsPanel(Panel, EM_ToolsPanel):
    bl_category = "EM"
    bl_idname = "VIEW3D_PT_ToolsPanel"
    bl_context = "objectmode"

#US/USV Manager
#####################################################################
#EMdb
class EMdbPanel:
    bl_label = "EMdb"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        row = layout.row()
        ob = context.object
        
        if len(scene.emdb_list) > 0:
            box = layout.box()
            row = box.row(align=True)
            split = row.split()
            col = split.column()
            col.label(text="Attività:")
            col = split.column(align=True)
            col.label(text=scene.emdb_list[scene.emdb_list_index].name)
            box = layout.box()
            row = box.row(align=True)
            split = row.split()
            col = split.column()
            col.label(text="Settore:")
            col = split.column(align=True)
            col.label(text=scene.emdb_list[scene.emdb_list_index].sector)
            box = layout.box()
            row = box.row(align=True)
            split = row.split()
            col = split.column()
            col.label(text="USM:")
            col = split.column(align=True)
            col.label(text=scene.emdb_list[scene.emdb_list_index].definition)
            box = layout.box()
            row = box.row(align=True)
            split = row.split()
            col = split.column()
            col.label(text="Materiali USM:")
            col = split.column(align=True)
            col.label(text=scene.emdb_list[scene.emdb_list_index].material)
            box = layout.box()
            row = box.row(align=True)
            split = row.split()
            col = split.column()
            col.label(text="Legante USM:")
            col = split.column(align=True)
            col.label(text=scene.emdb_list[scene.emdb_list_index].legante)
            box = layout.box()
            row = box.row(align=True)
            split = row.split()
            col = split.column()
            col.label(text="Funzione statica USM:")
            col = split.column(align=True)
            col.label(text=scene.emdb_list[scene.emdb_list_index].function)
            box = layout.box()
            row = box.row(align=True)
            split = row.split()
            col = split.column()
            col.label(text="US:")
            col = split.column(align=True)
            col.label(text=scene.emdb_list[scene.emdb_list_index].strato)
            box = layout.box()
            row = box.row(align=True)
            split = row.split()
            col = split.column()
            col.label(text="Interpretazione sintetica US:")
            col = split.column(align=True)
            col.label(text=scene.emdb_list[scene.emdb_list_index].interpretation)

        else:
            row = layout.row(align=True)
            row.label(text="Missing sqlite data")
        
        #row = layout.row(align=True)
        
        #col.prop(scene, "emdb_list_index", text='')

        #col.prop(scene, "emdb_list[scene.emdb_list_index].name", text='')

class VIEW3D_PT_EMdbPanel(Panel, EMdbPanel):
    bl_category = "EM"
    bl_idname = "VIEW3D_PT_EMdbPanel"
    bl_context = "objectmode"
#####################################################################
#Periods Manager
class EM_BasePanel:
    bl_label = "Periods Manager"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        row = layout.row()
        ob = context.object

        if len(scene.em_list) > 0:
            row.template_list(
                "EM_UL_named_epoch_managers", "", scene, "epoch_list", scene, "epoch_list_index")
            row = layout.row()
            row.label(text="Representation Models (RM):")
            op = row.operator("epoch_models.add_remove", text="", emboss=False, icon='ADD')
            op.rm_epoch = scene.epoch_list[scene.epoch_list_index].name
            op.rm_add = True
            op = row.operator("epoch_models.add_remove", text="", emboss=False, icon='REMOVE')
            op.rm_epoch = scene.epoch_list[scene.epoch_list_index].name
            op.rm_add = False
            op = row.operator("select_rm.given_epoch", text="", emboss=False, icon='SELECT_SET')
            op.rm_epoch = scene.epoch_list[scene.epoch_list_index].name
        else:
            row.label(text="No periods here :-(")
        
        row = layout.row()

        if ob is None:
            pass
        else:
            if ob.type in ['MESH']:
                row.label(text="Active object: "+ob.name)
                row = layout.row()

            if len(ob.EM_ep_belong_ob) > 0:
                row.template_list(
                    "EM_UL_belongob", "", ob, "EM_ep_belong_ob", ob, "EM_ep_belong_ob_index", rows=2)
            else:
                row.label(text="No periods for active object")

class VIEW3D_PT_BasePanel(Panel, EM_BasePanel):
    bl_category = "EM"
    bl_idname = "VIEW3D_PT_BasePanel"
    bl_context = "objectmode"

class EM_UL_named_epoch_managers(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        epoch_list = item
        #user_preferences = context.user_preferences
        #self.layout.prop(context.scene, "test_color", text='Detail Color')
        icons_style = 'OUTLINER'
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout = layout.split(factor=0.6, align=True)
            layout.prop(epoch_list, "name", text="", emboss=False)

            # select operator
            icon = 'RESTRICT_SELECT_ON' if epoch_list.is_selected else 'RESTRICT_SELECT_OFF'
            if icons_style == 'OUTLINER':
                icon = 'VIEWZOOM' if epoch_list.use_toggle else 'VIEWZOOM'
            layout = layout.split(factor=0.1, align=True)
            layout.prop(epoch_list, "epoch_RGB_color", text="", emboss=True, icon_value=0)
            op = layout.operator(
                "epoch_manager.toggle_select", text="", emboss=False, icon=icon)

            #self.layout.prop(context.scene, "test_color", text='Detail Color')
            op.group_em_idx = index
            # op.is_menu = False
            # op.is_select = True

            # lock operator
            icon = 'LOCKED' if epoch_list.is_locked else 'UNLOCKED'
            if icons_style == 'OUTLINER':
                icon = 'RESTRICT_SELECT_OFF' if epoch_list.is_locked else 'RESTRICT_SELECT_ON'
            op = layout.operator("epoch_manager.toggle_selectable", text="", emboss=False, icon=icon)
            #op.em_group_changer = 'LOCKING'
            op.group_em_idx = index

            # view operator
            icon = 'RESTRICT_VIEW_OFF' if epoch_list.use_toggle else 'RESTRICT_VIEW_ON'
            op = layout.operator(
                "epoch_manager.toggle_visibility", text="", emboss=False, icon=icon)
            op.group_em_vis_idx = index

            # view reconstruction
            icon = 'MESH_CUBE' if not epoch_list.reconstruction_on else 'SNAP_VOLUME'
            op = layout.operator(
                "epoch_manager.toggle_reconstruction", text="", emboss=False, icon=icon)
            op.group_em_vis_idx = index

            # soloing operator
            icon = 'RADIOBUT_ON' if epoch_list.epoch_soloing else 'RADIOBUT_OFF'
            op = layout.operator(
                "epoch_manager.toggle_soloing", text="", emboss=False, icon=icon)
            op.group_em_idx = index



            #icon = 'KEYTYPE_KEYFRAME_VEC' if epoch_list.rm_models else 'HANDLETYPE_FREE_VEC'
            #layout.label(icon=icon)

        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'

class EM_UL_belongob(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        split = layout.split()
        #split.label(text=str(item.epoch))
        split.prop(item, "epoch", text="", emboss=False, translate=False, icon='SORTTIME')

#Periods Manager
#####################################################################

#####################################################################
#Paradata Section

class EM_ParadataPanel:
    bl_label = "Paradata Manager"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        obj = context.object
        row = layout.row()

        # define variables 
        if scene.paradata_streaming_mode:
            property_list_var = "em_v_properties_list"
            property_list_index_var = "em_v_properties_list_index"
            property_list_cmd = "scene.em_v_properties_list"
            property_list_index_cmd = "scene.em_v_properties_list_index"

            combiner_list_var = "em_v_combiners_list"
            combiner_list_index_var = "em_v_combiners_list_index"
            combiner_list_cmd = "scene.em_v_combiners_list"
            combiner_list_index_cmd = "scene.em_v_combiners_list_index"

            extractor_list_var = "em_v_extractors_list"
            extractor_list_index_var = "em_v_extractors_list_index"
            extractor_list_cmd = "scene.em_v_extractors_list"
            extractor_list_index_cmd = "scene.em_v_extractors_list_index"

            source_list_var = "em_v_sources_list"
            source_list_index_var = "em_v_sources_list_index"
            source_list_cmd = "scene.em_v_sources_list"
            source_list_index_cmd = "scene.em_v_sources_list_index"

        else:
            property_list_var = "em_properties_list"
            property_list_index_var = "em_properties_list_index"
            property_list_cmd = "scene.em_properties_list"
            property_list_index_cmd = "scene.em_properties_list_index"

            combiner_list_var = "em_combiners_list"
            combiner_list_index_var = "em_combiners_list_index"
            combiner_list_cmd = "scene.em_combiners_list"
            combiner_list_index_cmd = "scene.em_combiners_list_index"

            extractor_list_var = "em_extractors_list"
            extractor_list_index_var = "em_extractors_list_index"
            extractor_list_cmd = "scene.em_extractors_list"
            extractor_list_index_cmd = "scene.em_extractors_list_index"  

            source_list_var = "em_sources_list"
            source_list_index_var = "em_sources_list_index"
            source_list_cmd = "scene.em_sources_list"
            source_list_index_cmd = "scene.em_sources_list_index"           

    ###############################################################################
    ##          Properties
    ###############################################################################

        len_property_var = "len("+property_list_cmd+")"
        if eval(property_list_index_cmd) >= 0 and eval(len_property_var) > 0:

            # layout.row().separator()

            row.label(text="Properties: ("+str(eval(len_property_var))+")")
            row.prop(scene, "prop_paradata_streaming_mode", text='', icon="SHORTDISPLAY")
            row = layout.row()
            row.template_list("EM_UL_properties_managers", "", scene, property_list_var, scene, property_list_index_var, rows=2)

            #item_source = scene.em_properties_list[scene.em_properties_list_index]
            item_property = eval(property_list_cmd)[eval(property_list_index_cmd)]
            box = layout.box()
            row = box.row(align=True)
            row = box.row()
            row.prop(item_property, "name", text="", icon='FILE_TEXT')
            row = box.row()
            row.prop(item_property, "description", text="", slider=True, emboss=True, icon='TEXT')
        else:
            row.label(text="No paradata here :-(")
    ###############################################################################
    ##          Combiners
    ###############################################################################

        len_combiner_var = "len("+combiner_list_cmd+")"
        if eval(combiner_list_index_cmd) >= 0 and eval(len_combiner_var) > 0:

            # layout.row().separator()

            row = layout.row()
            row.label(text="Reasoning - Combiners: ("+str(eval(len_combiner_var))+")")
            row.prop(scene, "comb_paradata_streaming_mode", text='', icon="SHORTDISPLAY")
            row = layout.row()
            row.template_list("EM_UL_combiners_managers", "", scene, combiner_list_var, scene, combiner_list_index_var, rows=1)
        
            item_property = eval(combiner_list_cmd)[eval(combiner_list_index_cmd)]
            box = layout.box()
            row = box.row(align=True)
            row = box.row()
            row.prop(item_property, "name", text="", icon='FILE_TEXT')
            row = box.row()
            row.prop(item_property, "description", text="", slider=True, emboss=True, icon='TEXT')
            row = box.row()
            row.prop(item_property, "url", text="", slider=True, emboss=True, icon='URL')
            op = row.operator("open.file", icon="EMPTY_SINGLE_ARROW", text='')
            op.node_type = combiner_list_var
            
    ###############################################################################
    ##          Extractors
    ###############################################################################

        len_source_var = "len("+extractor_list_cmd+")"
        if eval(extractor_list_index_cmd) >= 0 and eval(len_source_var) > 0:

            # layout.row().separator()

            row = layout.row()
            row.label(text="Interpretation - Extractors: ("+str(eval(len_source_var))+")")
            row.prop(scene, "extr_paradata_streaming_mode", text='', icon="SHORTDISPLAY")
            row = layout.row()
            row.template_list("EM_UL_extractors_managers", "", scene, extractor_list_var, scene, extractor_list_index_var, rows=2)

            item_source = eval(extractor_list_cmd)[eval(extractor_list_index_cmd)]
            box = layout.box()
            row = box.row(align=True)
            row = box.row()
            row.prop(item_source, "name", text="", icon='FILE_TEXT')
            op = row.operator("listitem.toobj", icon="PASTEDOWN", text='')
            op.list_type = extractor_list_var
            
            if scene.em_list[scene.em_list_index].icon == 'RESTRICT_INSTANCED_OFF':
                op = row.operator("select.fromlistitem", text='', icon="MESH_CUBE")
                op.list_type = extractor_list_var
            else:
                row.label(text="", icon='MESH_CUBE')
            if obj:
                if check_if_current_obj_has_brother_inlist(obj.name, extractor_list_var):
                    op = row.operator("select.listitem", text='', icon="LONGDISPLAY")
                    op.list_type = extractor_list_var
                else:
                    row.label(text="", icon='LONGDISPLAY')   
            
            row = box.row()
            row.prop(item_source, "description", text="", slider=True, emboss=True, icon='TEXT')
            row = box.row()
            row.prop(item_source, "url", text="", slider=True, emboss=True, icon='URL')
            op = row.operator("open.file", icon="EMPTY_SINGLE_ARROW", text='')
            op.node_type = extractor_list_var

    ###############################################################################
    ##          Sources
    ###############################################################################

        len_source_var = "len("+source_list_cmd+")"
        if eval(source_list_index_cmd) >= 0 and eval(len_source_var) > 0:

            # layout.row().separator()

            row = layout.row()
            row.label(text="Sources: ("+str(eval(len_source_var))+")")
            row = layout.row()
            row.template_list("EM_UL_sources_managers", "", scene, source_list_var, scene, source_list_index_var, rows=2)

            item_source = eval(source_list_cmd)[eval(source_list_index_cmd)]
            box = layout.box()
            row = box.row()
            row.prop(item_source, "name", text="", icon='FILE_TEXT')
            split = row.split()
            op = row.operator("listitem.toobj", icon="PASTEDOWN", text='')
            op.list_type = source_list_var
            
            #split = layout.split()
            if scene.em_list[scene.em_list_index].icon == 'RESTRICT_INSTANCED_OFF':
                #col = split.column()
                op = row.operator("select.fromlistitem", text='', icon="MESH_CUBE")
                op.list_type = source_list_var
            else:
                #col = split.column()
                row.label(text="", icon='MESH_CUBE')
            if obj:
                if check_if_current_obj_has_brother_inlist(obj.name, source_list_var):
                    #col = split.column(align=True)
                    op = row.operator("select.listitem", text='', icon="LONGDISPLAY")
                    op.list_type = source_list_var
                else:
                    #col = split.column()
                    row.label(text="", icon='LONGDISPLAY')              
            
            row = box.row()
            row.prop(item_source, "description", text="", slider=True, emboss=True, icon='TEXT')
            row = box.row()
            row.prop(item_source, "url", text="", slider=True, emboss=True, icon='URL')
            op = row.operator("open.file", icon="EMPTY_SINGLE_ARROW", text='')
            op.node_type = source_list_var
            row = box.row()

class VIEW3D_PT_ParadataPanel(Panel, EM_ParadataPanel):
    bl_category = "EM"
    bl_idname = "VIEW3D_PT_ParadataPanel"
    bl_context = "objectmode"

class EM_UL_sources_managers(UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        icons_style = 'OUTLINER'
        scene = context.scene
        layout = layout.split(factor =0.22, align = True)
        layout.label(text = item.name, icon = item.icon)
        layout.label(text = item.description, icon=item.icon_url)

class EM_UL_properties_managers(UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        icons_style = 'OUTLINER'
        scene = context.scene
        layout = layout.split(factor =0.4, align = True)
        layout.label(text = item.name)
        layout.label(text = item.description)

class EM_UL_combiners_managers(UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        icons_style = 'OUTLINER'
        scene = context.scene
        layout = layout.split(factor =0.25, align = True)
        layout.label(text = item.name)
        layout.label(text = item.description)

class EM_UL_extractors_managers(UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        icons_style = 'OUTLINER'
        scene = context.scene
        layout = layout.split(factor =0.25, align = True)
        layout.label(text = item.name, icon = item.icon)
        layout.label(text = item.description, icon=item.icon_url)

# Paradata section 
#####################################################################

#####################################################################
#Export Section

class EM_ExportPanel:
    bl_label = "Export Manager"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
 

        row = layout.row()
        box = layout.box()
        row = box.row()
        row.label(text="Tables export:")
        row = box.row()
        op = row.operator("export.uuss_export", text="EM (csv)", emboss=True, icon='LONGDISPLAY')
        row = box.row()
        row.prop(context.window_manager.export_tables_vars, 'table_type', expand=True)
        row = layout.row()
        box = layout.box()
        row = box.row()
        row.label(text="EMviq export:")
        row = box.row()
        row.prop(context.scene, 'EMviq_project_name', toggle=True, text="")
        row.label(text="<-- Project's name")
        row = box.row()#(align=True)
        row.prop(context.scene, 'EMviq_model_author_name', toggle=True, text="")
        row.label(text="<-- Model's author(s)")
        row = box.row()
        row.prop(context.scene, 'EMviq_user_name', toggle=True, text="")
        row.label(text="<-- ATON user's name")
        row = box.row()
        row.prop(context.scene, 'ATON_path', toggle=True, text="")
        row.label(text="<-- path to ATON")



        '''
        row = layout.row()  # (align=True)
        row.prop(context.scene, 'EMviq_folder', toggle=True, text="")
        row.label(text="<-- Collection folder export path")
        row = layout.row()#(align=True)
        row.prop(context.scene, 'EMviq_scene_folder', toggle=True, text="")
        row.label(text="<-- Scene folder export path")
        '''

        row = box.row()
        row.prop(context.window_manager.export_vars, 'format_file', expand=True)
        #box = layout.box()
        row = box.row()
        row.prop(context.scene, 'enable_image_compression', toggle = True, text='Use tex compression')
        row.prop(context.scene, 'EM_gltf_export_maxres', toggle = True, text='Max res')
        row.prop(context.scene, 'EM_gltf_export_quality', toggle = True, text='Size')
        row = box.row()
        op = row.operator("export_manager.export", text="Generate full EMviq Project", emboss=True, icon='LONGDISPLAY')
        op.em_export_type = 'EMviq'
        op.em_export_format = context.window_manager.export_vars.format_file

        row = box.row()
        row.label(text="Export partial Emviq project's components:")
        row = box.row()
        op = row.operator("export_manager.export", text="Proxies", emboss=True, icon='SHADING_SOLID')
        op.em_export_type = 'Proxies'
        op = row.operator("export_manager.export", text="GraphML", emboss=True, icon='SHADING_SOLID')
        op.em_export_type = 'GraphML'
        op = row.operator("export_manager.export", text="RM", emboss=True, icon='SHADING_TEXTURE')
        op.em_export_type = 'RM'

        row = layout.row()



        if scene.emviq_error_list_index >= 0 and len(scene.emviq_error_list) > 0:
            row.template_list("ER_UL_List", "EM nodes", scene, "emviq_error_list", scene, "emviq_error_list_index")
            item = scene.emviq_error_list[scene.emviq_error_list_index]
            box = layout.box()
            row = box.row(align=True)

            split = row.split()
            col = split.column()
            row.prop(item, "name", text="")
            split = row.split()
            col = split.column()
            op = col.operator("select.fromlistitem", text='', icon="MESH_CUBE")
            op.list_type = "emviq_error_list"
            #op = col.operator("listitem.toobj", icon="PASTEDOWN", text='')
            #op.list_type = "emviq_error_list"
            #row = layout.row()
            #row.label(text="Description:")
            row = box.row()
            #layout.alignment = 'LEFT'
            row.prop(item, "description", text="", slider=True, emboss=True)

class VIEW3D_PT_ExportPanel(Panel, EM_ExportPanel):
    bl_category = "EM"
    bl_idname = "VIEW3D_PT_ExportPanel"
    bl_context = "objectmode"


class ER_UL_List(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        icons_style = 'OUTLINER'
        scene = context.scene
        layout = layout.split(factor =0.30, align = True)
        layout.label(text = item.texture_type, icon = 'ERROR')
        layout.label(text = item.material, icon='NONE', icon_value=0)

#Export Section
#####################################################################