#!/usr/bin/python
from collections import OrderedDict

from NodeGraphQt.base.node import NodeObject
from NodeGraphQt.base.port import Port
from NodeGraphQt.constants import (NODE_PROP_QLABEL,
                                   NODE_PROP_QLINEEDIT,
                                   NODE_PROP_QCOMBO,
                                   NODE_PROP_QCHECKBOX,
                                   PortTypeEnum,
                                   NODE_LAYOUT_VERTICAL,
                                   NODE_LAYOUT_HORIZONTAL)
from NodeGraphQt.errors import (PortError,
                                PortRegistrationError,
                                NodeWidgetError)
from NodeGraphQt.qgraphics.node_base import NodeItem, NodeItemVertical
from NodeGraphQt.widgets.node_widgets import (NodeBaseWidget,
                                              NodeComboBox,
                                              NodeLineEdit,
                                              NodeCheckBox,
                                              NodeLabel)


class BaseNode(NodeObject):
    """
    The ``NodeGraphQt.BaseNode`` class is the base class for nodes that allows
    port connections from one node to another.

    **Inherited from:** :class:`NodeGraphQt.NodeObject`

    .. image:: ../_images/node.png
        :width: 250px

    example snippet:

    .. code-block:: python
        :linenos:

        from NodeGraphQt import BaseNode

        class ExampleNode(BaseNode):

            # unique node identifier domain.
            __identifier__ = 'io.jchanvfx.github'

            # initial default node name.
            NODE_NAME = 'My Node'

            def __init__(self):
                super(ExampleNode, self).__init__()

                # create an input port.
                self.add_input('in')

                # create an output port.
                self.add_output('out')
    """

    NODE_NAME = 'Node'

    def __init__(self, qgraphics_views=None):
        qgraphics_views = qgraphics_views or {
            NODE_LAYOUT_HORIZONTAL: NodeItem,
            NODE_LAYOUT_VERTICAL: NodeItemVertical
        }
        super(BaseNode, self).__init__(qgraphics_views)
        self._inputs = []
        self._outputs = []

    def draw(self):
        """
        Redraws the node in the scene.
        """
        self.view.draw_node()

    def update_model(self):
        """
        Update the node model from view.
        """
        for name, val in self.view.properties.items():
            if name in ['inputs', 'outputs']:
                continue
            self.model.set_property(name, val)

        for name, widget in self.view.widgets.items():
            self.model.set_property(name, widget.value)

    def set_icon(self, icon=None):
        """
        Set the node icon.

        Args:
            icon (str): path to the icon image.
        """
        self.set_property('icon', icon)

    def icon(self):
        """
        Node icon path.

        Returns:
            str: icon image file path.
        """
        return self.model.icon

    def widgets(self):
        """
        Returns all embedded widgets from this node.

        See Also:
            :meth:`BaseNode.get_widget`

        Returns:
            dict: embedded node widgets. {``property_name``: ``node_widget``}
        """
        return self.view.widgets

    def get_widget(self, name):
        """
        Returns the embedded widget associated with the property name.

        See Also:
            :meth:`BaseNode.add_combo_menu`,
            :meth:`BaseNode.add_text_input`,
            :meth:`BaseNode.add_checkbox`,

        Args:
            name (str): node property name.

        Returns:
            NodeBaseWidget: embedded node widget.
        """
        return self.view.widgets.get(name)

    def add_custom_widget(self, widget, widget_type=NODE_PROP_QLABEL, tab=None):
        """
        Add a custom node widget into the node.

        see example :ref:`Embedding Custom Widgets`.

        Note:
            The ``value_changed`` signal from the added node widget is wired
            up to the :meth:`NodeObject.set_property` function.

        Args:
            widget (NodeBaseWidget): node widget class object.
            widget_type: widget flag to display in the
                :class:`NodeGraphQt.PropertiesBinWidget` (default: QLabel).
            tab (str): name of the widget tab to display in.
        """
        if not isinstance(widget, NodeBaseWidget):
            raise NodeWidgetError(
                '\'widget\' must be an instance of a NodeBaseWidget')
        self.create_property(widget.get_name(),
                             widget.get_value(),
                             widget_type=widget_type,
                             tab=tab)
        widget.value_changed.connect(lambda k, v: self.set_property(k, v))
        widget._node = self
        self.view.add_widget(widget)

    def add_combo_menu(self, name, label='', items=None, tab=None):
        """
        Creates a custom property with the :meth:`NodeObject.create_property`
        function and embeds a :class:`PySide2.QtWidgets.QComboBox` widget
        into the node.

        Note:
            The ``value_changed`` signal from the added node widget is wired
            up to the :meth:`NodeObject.set_property` function.

        Args:
            name (str): name for the custom property.
            label (str): label to be displayed.
            items (list[str]): items to be added into the menu.
            tab (str): name of the widget tab to display in.
        """
        items = items or []
        self.create_property(
            name, items[0], items=items, widget_type=NODE_PROP_QCOMBO, tab=tab)

        widget = NodeComboBox(self.view, name, label, items)
        widget.value_changed.connect(lambda k, v: self.set_property(k, v))
        self.view.add_widget(widget)

    def add_text_input(self, name, label='', text='', tab=None):
        """
        Creates a custom property with the :meth:`NodeObject.create_property`
        function and embeds a :class:`PySide2.QtWidgets.QLineEdit` widget
        into the node.

        Note:
            The ``value_changed`` signal from the added node widget is wired
            up to the :meth:`NodeObject.set_property` function.

        Args:
            name (str): name for the custom property.
            label (str): label to be displayed.
            text (str): pre filled text.
            tab (str): name of the widget tab to display in.
        """
        self.create_property(
            name, text, widget_type=NODE_PROP_QLINEEDIT, tab=tab)
        widget = NodeLineEdit(self.view, name, label, text)
        widget.value_changed.connect(lambda k, v: self.set_property(k, v))
        self.view.add_widget(widget)

    def add_checkbox(self, name, label='', text='', state=False, tab=None):
        """
        Creates a custom property with the :meth:`NodeObject.create_property`
        function and embeds a :class:`PySide2.QtWidgets.QCheckBox` widget
        into the node.

        Note:
            The ``value_changed`` signal from the added node widget is wired
            up to the :meth:`NodeObject.set_property` function.

        Args:
            name (str): name for the custom property.
            label (str): label to be displayed.
            text (str): checkbox text.
            state (bool): pre-check.
            tab (str): name of the widget tab to display in.
        """
        self.create_property(
            name, state, widget_type=NODE_PROP_QCHECKBOX, tab=tab)
        widget = NodeCheckBox(self.view, name, label, text, state)
        widget.value_changed.connect(lambda k, v: self.set_property(k, v))
        self.view.add_widget(widget)

    def add_label(self, name, text='', tab=None):
        """
        Creates a custom property with the :meth:`NodeObject.create_property`
        function and embeds a :class:`PySide2.QtWidgets.QLabel` widget
        into the node.

        Args:
            name (str): name for the custom property.
            text (str): label text to be displayed.
            tab (str): name of the widget tab to display in.
        """
        self.create_property(
            name, text, widget_type=NODE_PROP_QLABEL, tab=tab)
        widget = NodeLabel(self.view, name, text)
        self.view.add_widget(widget)

    def add_input(self, name='input', multi_input=False, display_name=True,
                  color=None, locked=False, painter_func=None):
        """
        Add input :class:`Port` to node.

        Warnings:
            Undo is NOT supported for this function.

        Args:
            name (str): name for the input port.
            multi_input (bool): allow port to have more than one connection.
            display_name (bool): display the port name on the node.
            color (tuple): initial port color (r, g, b) ``0-255``.
            locked (bool): locked state see :meth:`Port.set_locked`
            painter_func (function or None): custom function to override the drawing
                of the port shape see example: :ref:`Creating Custom Shapes`

        Returns:
            NodeGraphQt.Port: the created port object.
        """
        if name in self.inputs().keys():
            raise PortRegistrationError(
                'port name "{}" already registered.'.format(name))

        port_args = [name, multi_input, display_name, locked]
        if painter_func and callable(painter_func):
            port_args.append(painter_func)
        view = self.view.add_input(*port_args)

        if color:
            view.color = color
            view.border_color = [min([255, max([0, i + 80])]) for i in color]

        port = Port(self, view)
        port.model.type_ = PortTypeEnum.IN.value
        port.model.name = name
        port.model.display_name = display_name
        port.model.multi_connection = multi_input
        port.model.locked = locked
        self._inputs.append(port)
        self.model.inputs[port.name()] = port.model
        return port

    def add_output(self, name='output', multi_output=True, display_name=True,
                   color=None, locked=False, painter_func=None):
        """
        Add output :class:`Port` to node.

        Warnings:
            Undo is NOT supported for this function.

        Args:
            name (str): name for the output port.
            multi_output (bool): allow port to have more than one connection.
            display_name (bool): display the port name on the node.
            color (tuple): initial port color (r, g, b) ``0-255``.
            locked (bool): locked state see :meth:`Port.set_locked`
            painter_func (function or None): custom function to override the drawing
                of the port shape see example: :ref:`Creating Custom Shapes`

        Returns:
            NodeGraphQt.Port: the created port object.
        """
        if name in self.outputs().keys():
            raise PortRegistrationError(
                'port name "{}" already registered.'.format(name))

        port_args = [name, multi_output, display_name, locked]
        if painter_func and callable(painter_func):
            port_args.append(painter_func)
        view = self.view.add_output(*port_args)

        if color:
            view.color = color
            view.border_color = [min([255, max([0, i + 80])]) for i in color]
        port = Port(self, view)
        port.model.type_ = PortTypeEnum.OUT.value
        port.model.name = name
        port.model.display_name = display_name
        port.model.multi_connection = multi_output
        port.model.locked = locked
        self._outputs.append(port)
        self.model.outputs[port.name()] = port.model
        return port

    def get_input(self, port):
        """
        Get input port by the name or index.

        Args:
            port (str or int): port name or index.

        Returns:
            NodeGraphQt.Port: node port.
        """
        if type(port) is int:
            if port < len(self._inputs):
                return self._inputs[port]
        elif type(port) is str:
            return self.inputs().get(port, None)

    def get_output(self, port):
        """
        Get output port by the name or index.

        Args:
            port (str or int): port name or index.

        Returns:
            NodeGraphQt.Port: node port.
        """
        if type(port) is int:
            if port < len(self._outputs):
                return self._outputs[port]
        elif type(port) is str:
            return self.outputs().get(port, None)

    def delete_input(self, port):
        """
        Delete input port.

        Warnings:
            Undo is NOT supported for this function.

            You can only delete ports if :meth:`BaseNode.port_deletion_allowed`
            returns ``True`` otherwise a port error is raised see also
            :meth:`BaseNode.set_port_deletion_allowed`.

        Args:
            port (str or int): port name or index.
        """
        if type(port) in [int, str]:
            port = self.get_input(port)
            if port is None:
                return
        if not self.port_deletion_allowed():
            raise PortError(
                'Port "{}" can\'t be deleted on this node because '
                '"ports_removable" is not enabled.'.format(port.name()))
        if port.locked():
            raise PortError('Error: Can\'t delete a port that is locked!')
        self._inputs.remove(port)
        self._model.inputs.pop(port.name())
        self._view.delete_input(port.view)
        port.model.node = None
        self.draw()

    def delete_output(self, port):
        """
        Delete output port.

        Warnings:
            Undo is NOT supported for this function.

            You can only delete ports if :meth:`BaseNode.port_deletion_allowed`
            returns ``True`` otherwise a port error is raised see also
            :meth:`BaseNode.set_port_deletion_allowed`.

        Args:
            port (str or int): port name or index.
        """
        if type(port) in [int, str]:
            port = self.get_output(port)
            if port is None:
                return
        if not self.port_deletion_allowed():
            raise PortError(
                'Port "{}" can\'t be deleted on this node because '
                '"ports_removable" is not enabled.'.format(port.name()))
        if port.locked():
            raise PortError('Error: Can\'t delete a port that is locked!')
        self._outputs.remove(port)
        self._model.outputs.pop(port.name())
        self._view.delete_output(port.view)
        port.model.node = None
        self.draw()

    def set_port_deletion_allowed(self, mode=False):
        """
        Allow ports to be removable on this node.

        See Also:
            :meth:`BaseNode.port_deletion_allowed` and
            :meth:`BaseNode.set_ports`

        Args:
            mode (bool): true to allow.
        """
        self.model.port_deletion_allowed = mode

    def port_deletion_allowed(self):
        """
        Return true if ports can be deleted on this node.

        See Also:
            :meth:`BaseNode.set_port_deletion_allowed`

        Returns:
            bool: true if ports can be deleted.
        """
        return self.model.port_deletion_allowed

    def set_ports(self, port_data):
        """
        Create node input and output ports from serialized port data.

        Warnings:
            You can only use this function if the node has
            :meth:`BaseNode.port_deletion_allowed` is `True`
            see :meth:`BaseNode.set_port_deletion_allowed`

        Hint:
            example snippet of port data.

            .. highlight:: python
            .. code-block:: python

                {
                    'input_ports':
                        [{
                            'name': 'input',
                            'multi_connection': True,
                            'display_name': 'Input',
                            'locked': False
                        }],
                    'output_ports':
                        [{
                            'name': 'output',
                            'multi_connection': True,
                            'display_name': 'Output',
                            'locked': False
                        }]
                }

        Args:
            port_data(dict): port data.
        """
        if not self.port_deletion_allowed():
            raise PortError(
                'Ports cannot be set on this node because '
                '"set_port_deletion_allowed" is not enabled on this node.')

        for port in self._inputs:
            self._view.delete_input(port.view)
            port.model.node = None
        for port in self._outputs:
            self._view.delete_output(port.view)
            port.model.node = None
        self._inputs = []
        self._outputs = []
        self._model.outputs = {}
        self._model.inputs = {}

        [self.add_input(name=port['name'],
                        multi_input=port['multi_connection'],
                        display_name=port['display_name'],
                        locked=port.get('locked') or False)
         for port in port_data['input_ports']]
        [self.add_output(name=port['name'],
                         multi_output=port['multi_connection'],
                         display_name=port['display_name'],
                         locked=port.get('locked') or False)
         for port in port_data['output_ports']]
        self.draw()

    def inputs(self):
        """
        Returns all the input ports from the node.

        Returns:
            dict: {<port_name>: <port_object>}
        """
        return {p.name(): p for p in self._inputs}

    def input_ports(self):
        """
        Return all input ports.

        Returns:
            list[NodeGraphQt.Port]: node input ports.
        """
        return self._inputs

    def outputs(self):
        """
        Returns all the output ports from the node.

        Returns:
            dict: {<port_name>: <port_object>}
        """
        return {p.name(): p for p in self._outputs}

    def output_ports(self):
        """
        Return all output ports.

        Returns:
            list[NodeGraphQt.Port]: node output ports.
        """
        return self._outputs

    def input(self, index):
        """
        Return the input port with the matching index.

        Args:
            index (int): index of the input port.

        Returns:
            NodeGraphQt.Port: port object.
        """
        return self._inputs[index]

    def set_input(self, index, port):
        """
        Creates a connection pipe to the targeted output :class:`Port`.

        Args:
            index (int): index of the port.
            port (NodeGraphQt.Port): port object.
        """
        src_port = self.input(index)
        src_port.connect_to(port)

    def output(self, index):
        """
        Return the output port with the matching index.

        Args:
            index (int): index of the output port.

        Returns:
            NodeGraphQt.Port: port object.
        """
        return self._outputs[index]

    def set_output(self, index, port):
        """
        Creates a connection pipe to the targeted input :class:`Port`.

        Args:
            index (int): index of the port.
            port (NodeGraphQt.Port): port object.
        """
        src_port = self.output(index)
        src_port.connect_to(port)

    def connected_input_nodes(self):
        """
        Returns all nodes connected from the input ports.

        Returns:
            dict: {<input_port>: <node_list>}
        """
        nodes = OrderedDict()
        for p in self.input_ports():
            nodes[p] = [cp.node() for cp in p.connected_ports()]
        return nodes

    def connected_output_nodes(self):
        """
        Returns all nodes connected from the output ports.

        Returns:
            dict: {<output_port>: <node_list>}
        """
        nodes = OrderedDict()
        for p in self.output_ports():
            nodes[p] = [cp.node() for cp in p.connected_ports()]
        return nodes

    def on_input_connected(self, in_port, out_port):
        """
        Callback triggered when a new pipe connection is made.

        *The default of this function does nothing re-implement if you require
        logic to run for this event.*

        Note:
            to work with undo & redo for this method re-implement
            :meth:`BaseNode.on_input_disconnected` with the reverse logic.

        Args:
            in_port (NodeGraphQt.Port): source input port from this node.
            out_port (NodeGraphQt.Port): output port that connected to this node.
        """
        return

    def on_input_disconnected(self, in_port, out_port):
        """
        Callback triggered when a pipe connection has been disconnected
        from a INPUT port.

        *The default of this function does nothing re-implement if you require
        logic to run for this event.*

        Note:
            to work with undo & redo for this method re-implement
            :meth:`BaseNode.on_input_connected` with the reverse logic.

        Args:
            in_port (NodeGraphQt.Port): source input port from this node.
            out_port (NodeGraphQt.Port): output port that was disconnected.
        """
        return
