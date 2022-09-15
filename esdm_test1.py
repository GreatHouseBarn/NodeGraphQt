#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import signal

from Qt import QtCore, QtWidgets

from NodeGraphQt import (
    NodeGraph,
    PropertiesBinWidget,
    NodesTreeWidget,
    NodesPaletteWidget
)
from NodeGraphQt.constants import NODE_PROP_QLABEL, ViewerEnum, NODE_LAYOUT_HORIZONTAL, NODE_LAYOUT_VERTICAL

# import example nodes from the "example_nodes" package
from examples import group_node
from examples.custom_nodes import (
    basic_nodes,
    custom_ports_node,
    network_nodes,
    widget_nodes
)

if __name__ == '__main__':
    # handle SIGINT to make the app terminate on CTRL+C
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

    app = QtWidgets.QApplication([])

    # create graph controller.
    graph = NodeGraph()
    graph.set_background_color(252, 252, 252)
    graph.set_grid_color(248, 248, 248)
    graph.set_grid_mode(ViewerEnum.GRID_DISPLAY_NONE)

    graph.set_acyclic()


    # registered example nodes.
    graph.register_nodes([
        # basic_nodes.BasicNodeA,
        # basic_nodes.BasicNodeB,
        # custom_ports_node.CustomPortsNode,
        # group_node.MyGroupNode,
        # widget_nodes.DropdownMenuNode,
        # widget_nodes.TextInputNode,
        # widget_nodes.CheckboxNode,
        network_nodes.TrunkInNode,
        network_nodes.TrunkOutNode,
        network_nodes.Splitter1x4Node,
        network_nodes.Splitter1x8Node,
        network_nodes.Splitter1x16Node,
        network_nodes.Splitter1x32Node
    ])

    # show the node graph widget.
    graph_widget = graph.widget
    graph_widget.resize(1400, 1000)
    graph_widget.show()

    # create node with custom text color and disable it.
    # n_basic_a = graph.create_node(
    #     'nodes.basic.BasicNodeA', text_color='#feab20')
    # n_basic_a.set_disabled(True)

    # create node and set a custom icon.
    # n_basic_b = graph.create_node(
    #     'nodes.basic.BasicNodeB', name='custom icon')
    # this_path = os.path.dirname(os.path.abspath(__file__))
    # icon = os.path.join(this_path, 'examples', 'star.png')
    # n_basic_b.set_icon(icon)

    # create node with the custom port shapes.
    # n_custom_ports = graph.create_node(
    #     'nodes.custom.ports.CustomPortsNode', name='custom ports')

    # create node with the embedded QLineEdit widget.
    # n_text_input = graph.create_node(
    #     'nodes.widget.TextInputNode', name='text node', color='#0a1e20')

    # create node with the embedded QCheckBox widgets.
    # n_checkbox = graph.create_node(
    #     'nodes.widget.CheckboxNode', name='checkbox node')

    # create node with the QComboBox widget.
    # n_combo_menu = graph.create_node(
    #     'nodes.widget.DropdownMenuNode', name='combobox node')

    # create group node.
    # n_group = graph.create_node('nodes.group.MyGroupNode')

    # make node connections.

    # (connect nodes using the .set_output method)
    # n_text_input.set_output(0, n_custom_ports.input(0))
    # n_text_input.set_output(0, n_checkbox.input(0))
    # n_text_input.set_output(0, n_combo_menu.input(0))
    # # (connect nodes using the .set_input method)
    # n_group.set_input(0, n_custom_ports.output(1))
    # n_basic_b.set_input(2, n_checkbox.output(0))
    # n_basic_b.set_input(2, n_combo_menu.output(1))
    # (connect nodes using the .connect_to method from the port object)
    # port = n_basic_a.input(0)
    # port.connect_to(n_basic_b.output(0))


    n_trunk_out = graph.create_node('nodes.network.TrunkOutNode',color='#fafafa',text_color='#000000')
    n_trunk_out.create_property('Label:', 'XYZ-123-116/2022/A', widget_type=NODE_PROP_QLABEL, tab='Data')
    n_trunk_out.create_property('GPS Loc:', '51.2N 3W', widget_type=NODE_PROP_QLABEL, tab='Data')
    # n_trunk_out.add_text_input('my_input', 'Text Input', tab='widgets')

    n_trunk_in = graph.create_node('nodes.network.TrunkInNode',color='#fafafa',text_color='#000000')

    for i in range(12):
        n_trunk_out.set_output(i, n_trunk_in.input(i))

    n_split_4 = graph.create_node('nodes.network.Splitter1x4Node',color='#fafafa',text_color='#000000')

    # auto layout nodes.
    graph.auto_layout_nodes()

    # crate a backdrop node and wrap it around
    # "custom port node" and "group node".
    # n_backdrop = graph.create_node('Backdrop')
    # n_backdrop.wrap_nodes([n_custom_ports, n_combo_menu])

    # fit node selection to the viewer.
    graph.fit_to_selection()

    # Custom builtin widgets from NodeGraphQt
    # ---------------------------------------

    # create a node properties bin widget.
    properties_bin = PropertiesBinWidget(node_graph=graph)
    properties_bin.setWindowFlags(QtCore.Qt.Tool)

    # example show the node properties bin widget when a node is double clicked.
    def display_properties_bin(node):
        if not properties_bin.isVisible():
            properties_bin.show()

    # wire function to "node_double_clicked" signal.
    graph.node_double_clicked.connect(display_properties_bin)

    # # create a nodes tree widget.
    # nodes_tree = NodesTreeWidget(node_graph=graph)
    # nodes_tree.set_category_label('nodeGraphQt.nodes', 'Builtin Nodes')
    # nodes_tree.set_category_label('nodes.custom.ports', 'Custom Port Nodes')
    # nodes_tree.set_category_label('nodes.widget', 'Widget Nodes')
    # nodes_tree.set_category_label('nodes.basic', 'Basic Nodes')
    # nodes_tree.set_category_label('nodes.group', 'Group Nodes')
    # nodes_tree.set_category_label('nodes.network', 'Network Nodes')
    # nodes_tree.show()

    # # create a node palette widget.
    # nodes_palette = NodesPaletteWidget(node_graph=graph)
    # nodes_palette.set_category_label('nodeGraphQt.nodes', 'Builtin Nodes')
    # nodes_palette.set_category_label('nodes.custom.ports', 'Custom Port Nodes')
    # nodes_palette.set_category_label('nodes.widget', 'Widget Nodes')
    # nodes_palette.set_category_label('nodes.basic', 'Basic Nodes')
    # nodes_palette.set_category_label('nodes.group', 'Group Nodes')
    # nodes_palette.set_category_label('nodes.network', 'Network Nodes')
    # nodes_palette.show()

    app.exec_()
