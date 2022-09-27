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
    graph.set_grid_mode(ViewerEnum.GRID_DISPLAY_NONE.value)

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
        network_nodes.Splitter1x32Node,
        network_nodes.DPInNode,
        network_nodes.DPOutNode,
        network_nodes.MDUNode
    ])

    # show the node graph widget.
    graph_widget = graph.widget
    graph_widget.resize(1400, 1000)
    graph_widget.show()

    n_dp_out = []
    n_dp_in = []
    n_trunk_out = []
    n_trunk_in = []
    n_mdu = []
    n_split = []


    n = graph.create_node('nodes.network.TrunkOutNode',color='#fafafa',text_color='#000000', selected=False)
    n.set_property('label', 'XYZ-123-116/2022/A')
    n_trunk_out.append(n)

    n = graph.create_node('nodes.network.DPOutNode',color='#fafafa',text_color='#000000', selected=False)
    n.set_property('label', 'To DP SC03')
    n.set_input(0, n_trunk_out[0].output(0))
    n_dp_out.append(n)

    n = graph.create_node('nodes.network.TrunkInNode',color='#fafafa',text_color='#000000', selected=False)
    n.set_property('label', 'aaaXYZ-123-116 / 2021 / A16652 / JJ')
    n_trunk_in.append(n)

    n = graph.create_node('nodes.network.DPInNode',color='#fafafa',text_color='#000000', selected=False)
    n.set_property('label', 'From DP SC57')
    n.set_output(0, n_trunk_in[0].input(0))
    n_dp_in.append(n)

    #graph.auto_layout_nodes()

    n = graph.create_node('nodes.network.Splitter1x8Node',color='#fafafa',text_color='#000000', selected=False)
    n.set_property('label', 'SC02/SP1')
    n.set_input(0, n_trunk_in[0].output(1))
    n.set_output(0, n_trunk_out[0].input(0))
    n.set_output(1, n_trunk_out[0].input(1))
    n.set_output(2, n_trunk_out[0].input(2))
    n_split.append(n)

    n = graph.create_node('nodes.network.Splitter1x8Node',color='#fafafa',text_color='#000000', selected=False)
    n.set_property('label', 'SC02/SP2')
    n.set_input(0, n_trunk_in[0].output(2))
    n_split.append(n)

    n = graph.create_node('nodes.network.TrunkOutNode',color='#fafafa',text_color='#000000', selected=False)
    n.set_property('label', 'To MDU')
    n.set_input(0, n_split[0].output(3))
    n.set_input(1, n_split[0].output(4))
    n.set_input(2, n_split[0].output(5))
    n.set_input(3, n_split[0].output(6))
    n_trunk_out.append(n)

    n = graph.create_node('nodes.network.MDUNode',color='#fafafa',text_color='#000000', selected=False)
    n.set_property('label', 'MDU 4/46 DFE03.2.DP.AB.20 4 Homes')
    n.set_input(0, n_trunk_out[1].output(0))

    n = graph.create_node('nodes.network.TrunkOutNode',color='#fafafa',text_color='#000000', selected=False)
    n.set_property('label', 'To MDU')
    n.set_input(0, n_split[0].output(7))
    n.set_input(1, n_split[1].output(1))
    n.set_input(2, n_split[1].output(2))
    n_trunk_out.append(n)

    n = graph.create_node('nodes.network.MDUNode',color='#fafafa',text_color='#000000', selected=False)
    n.set_property('label', 'MDU 4/153 DFE03.2.DP.AB.21 3 Homes')
    n.set_input(0, n_trunk_out[2].output(0))

    n = graph.create_node('nodes.network.TrunkOutNode',color='#fafafa',text_color='#000000', selected=False)
    n.set_property('label', 'To MDU')
    n.set_input(0, n_split[1].output(2))
    n.set_input(1, n_split[1].output(3))
    n.set_input(2, n_split[1].output(4))
    n.set_input(3, n_split[1].output(5))
    n.set_input(4, n_split[1].output(6))
    n.set_input(5, n_split[1].output(7))
    n_trunk_out.append(n)

    n = graph.create_node('nodes.network.MDUNode',color='#fafafa',text_color='#000000', selected=False)
    n.set_property('label', 'MDU 8/107 DFE03.2.DP.AB.4 6 Homes')
    n.set_input(0, n_trunk_out[3].output(0))

    graph.auto_layout_nodes()

    # put all the trunk terminatores and splitters into a box
    n_backdrop = graph.create_node('Backdrop','SC03')
    n_backdrop.wrap_nodes(n_trunk_in + n_trunk_out + n_split)

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
