from cortix.src.port import Port
from cortix.src.cortix_main import Cortix

from cortix.util.dataplot import DataPlot
from stack_receiver import Receiver

# Init the modules
cortix = Cortix(use_mpi=False)
data_plot = DataPlot()
receiver = Receiver()

# Create the ports
serial_port = Port("serial")
plot_serial = Port("plot-serial")
serial_port.connect(plot_serial)

# Add the ports to the modules
receiver.add_port(serial_port)
data_plot.add_port(plot_serial)

# Add the modules to Cortix
cortix.add_module(receiver)
cortix.add_module(data_plot)

cortix.run()
