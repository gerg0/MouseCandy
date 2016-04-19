import controlpanel
import mclass
import mconfig
mconfig.GPIO_init()

from time import sleep

#cp = controlpanel.ControlPanel()
#cp.start_checking()

example = mclass.OlfactoryGng("Test project", "", "on", \
			20, 10, 3, 0.2, 2, 3, "on", \
			"A", "B", "C", 1.5)

#cp.set_text(str(example))
#cp.animation("Waiting...")

from mvalve import Valve
v1 = Valve(mconfig.odor_pin['A'])
v2 = Valve(mconfig.odor_pin['B'])

sleep(5)
v1.pulse()
v2.pulse()

