# =============================================================================
# OOP in Python — Equipment Maintenance Example
# =============================================================================
# This file walks through the core OOP concepts using a simple equipment
# tracking system — the kind of thing you'd actually use in a FAB environment.
#
# Concepts covered:
#   1. Classes and instances
#   2. __init__ (constructor)
#   3. Instance attributes and methods
#   4. Encapsulation (_private convention)
#   5. Inheritance (parent -> child class)
#   6. super() — calling the parent class
#   7. Method overriding
#   8. A simple list-based "registry" to tie it all together
# =============================================================================


# =============================================================================
# PART 1 — The base class: Equipment
# =============================================================================
#
# Think of a class like a FUNCTION_BLOCK definition in ST.
# It describes what data an object holds and what it can do.
# No memory is allocated yet — this is just the blueprint.

class Equipment:
    """
    Base class for all equipment in the FAB.
    Every piece of equipment shares these basic attributes and methods.
    """

    # -------------------------------------------------------------------------
    # __init__ is the constructor — it runs automatically when you create
    # a new object from this class. In ST this is like declaring your VAR block.
    #
    # 'self' is a reference to the specific instance being created.
    # Every method in a class must have 'self' as its first parameter.
    # You never pass it manually — Python handles that automatically.
    # -------------------------------------------------------------------------
    def __init__(self, tag: str, name: str, location: str):
        # These are INSTANCE ATTRIBUTES — each object gets its own copy.
        # Syntax: self.attribute_name = value
        self.tag = tag              # e.g. "P-201"
        self.name = name            # e.g. "Diffusion Pump 1"
        self.location = location    # e.g. "Bay 3"

        # Attributes don't have to come from parameters.
        # These are set to default values at creation time.
        self.fault = False          # no fault at startup
        self.fault_message = ""     # empty fault description
        self._maintenance_log = []  # internal log — see encapsulation note below

    # -------------------------------------------------------------------------
    # ENCAPSULATION: The leading underscore on _maintenance_log signals
    # "this is internal — don't access it directly from outside the class."
    # Python doesn't enforce this, but it's a strong convention everyone follows.
    # In ST you'd use VAR for this kind of internal state.
    # -------------------------------------------------------------------------

    def set_fault(self, message: str):
        """Set the equipment into a fault state with a description."""
        self.fault = True
        self.fault_message = message
        print(f"[FAULT] {self.tag} — {message}")

    def reset_fault(self):
        """Clear the fault state."""
        self.fault = False
        self.fault_message = ""
        print(f"[OK]    {self.tag} fault cleared")

    def log_maintenance(self, entry: str):
        """Add a maintenance entry to the internal log."""
        # We access _maintenance_log here because we ARE inside the class.
        # From outside, you'd call this method instead of touching the list directly.
        self._maintenance_log.append(entry)
        print(f"[LOG]   {self.tag}: '{entry}' logged")

    def show_log(self):
        """Print all maintenance entries."""
        print(f"\n--- Maintenance log for {self.tag} ({self.name}) ---")
        if not self._maintenance_log:
            print("  No entries.")
        else:
            for i, entry in enumerate(self._maintenance_log, start=1):
                print(f"  {i}. {entry}")

    def info(self):
        """Print a summary of this equipment's status."""
        # f-strings let you embed variables directly in strings: f"text {variable} text"
        fault_str = f"FAULT: {self.fault_message}" if self.fault else "OK"
        print(f"[{self.tag}] {self.name} | Location: {self.location} | Status: {fault_str}")


# =============================================================================
# PART 2 — Child class: Pump
# Inherits from Equipment — like EXTENDS in ST
# =============================================================================

class Pump(Equipment):      # <-- the part in () means "inherit from Equipment"
    """
    A pump is a type of Equipment, so it inherits everything from it.
    We add pump-specific attributes (flow rate, running state) on top.
    """

    def __init__(self, tag: str, name: str, location: str, flow_rate_lpm: float):
        # super().__init__(...) calls the PARENT class constructor first.
        # This is exactly like SUPER^() in ST — it sets up the base attributes
        # (tag, name, location, fault, _maintenance_log) before we add our own.
        super().__init__(tag, name, location)

        # Now add Pump-specific attributes
        self.flow_rate_lpm = flow_rate_lpm  # rated flow in litres/min
        self.running = False                # pump is off by default
        self._run_hours = 0.0              # internal hour counter

    def start(self):
        """Start the pump — checks for faults first."""
        if self.fault:
            print(f"[WARN]  {self.tag} cannot start — active fault: {self.fault_message}")
            return  # 'return' exits the method early, like RETURN in ST
        if self.running:
            print(f"[INFO]  {self.tag} is already running")
            return
        self.running = True
        print(f"[START] {self.tag} started at {self.flow_rate_lpm} L/min")

    def stop(self):
        """Stop the pump."""
        if not self.running:
            print(f"[INFO]  {self.tag} is already stopped")
            return
        self.running = False
        print(f"[STOP]  {self.tag} stopped")

    def add_run_hours(self, hours: float):
        """Add operating hours to the internal counter."""
        self._run_hours += hours

    def info(self):
        """
        Override the parent info() method to include pump-specific details.
        We call super().info() first so we don't lose the base output.
        """
        super().info()      # prints the Equipment line first
        state = "RUNNING" if self.running else "STOPPED"
        print(f"         Flow: {self.flow_rate_lpm} L/min | State: {state} | Run hours: {self._run_hours:.1f} h")


# =============================================================================
# PART 3 — Another child class: Sensor
# Shows how multiple different child classes can share the same parent
# =============================================================================

class Sensor(Equipment):
    """
    A sensor is also a type of Equipment.
    It holds a measured value and raises a fault if out of range.
    """

    def __init__(self, tag: str, name: str, location: str,
                unit: str, low_limit: float, high_limit: float):
        super().__init__(tag, name, location)   # same pattern as Pump

        self.unit = unit
        self.low_limit = low_limit
        self.high_limit = high_limit
        self._value = 0.0           # current measured value (private)

    def update(self, new_value: float):
        """
        Update the sensor reading.
        Automatically raises a fault if the value is out of range.
        """
        self._value = new_value

        # Range check — calls the inherited set_fault() from Equipment
        if new_value < self.low_limit:
            self.set_fault(f"Value {new_value} {self.unit} below low limit {self.low_limit}")
        elif new_value > self.high_limit:
            self.set_fault(f"Value {new_value} {self.unit} above high limit {self.high_limit}")
        else:
            # If it was in fault before and is now OK, auto-clear
            if self.fault:
                self.reset_fault()

    def read(self) -> float:
        """Return the current measured value."""
        return self._value

    def info(self):
        """Override info() to show the current reading."""
        super().info()
        print(f"         Value: {self._value:.2f} {self.unit} | Range: {self.low_limit}–{self.high_limit} {self.unit}")


# =============================================================================
# PART 4 — Equipment Registry
# A simple class that holds a list of equipment objects.
# This shows how objects work together.
# =============================================================================

class EquipmentRegistry:
    """
    Manages a collection of Equipment objects.
    Like a simple CMMS (Computerized Maintenance Management System).
    """

    def __init__(self):
        # A plain list that holds any Equipment object (or subclass of it)
        self._equipment = []

    def add(self, item: Equipment):
        """Add an equipment object to the registry."""
        self._equipment.append(item)
        print(f"[REG]   Added: {item.tag} — {item.name}")

    def find(self, tag: str) -> Equipment:
        """
        Find an equipment item by its tag. Returns the object or None.
        This is a linear search — fine for small lists.
        """
        for item in self._equipment:
            if item.tag == tag:
                return item     # return the actual object — you can then call methods on it
        return None             # nothing found

    def show_all(self):
        """Print a status summary for every registered item."""
        print("\n========== EQUIPMENT STATUS ==========")
        for item in self._equipment:
            item.info()         # calls the correct info() for each type (polymorphism!)
        print("======================================\n")

    def show_faults(self):
        """Print only the items that currently have a fault."""
        faulted = [item for item in self._equipment if item.fault]
        # The line above is a LIST COMPREHENSION — a compact way to filter a list.
        # It's equivalent to:
        #   faulted = []
        #   for item in self._equipment:
        #       if item.fault:
        #           faulted.append(item)

        print(f"\n========== ACTIVE FAULTS ({len(faulted)}) ==========")
        if not faulted:
            print("  No active faults.")
        else:
            for item in faulted:
                print(f"  [{item.tag}] {item.name}: {item.fault_message}")
        print()


# =============================================================================
# PART 5 — Main script
# This is where we actually create objects and use them.
# The 'if __name__ == "__main__"' block means:
#   "only run this code if this file is executed directly"
#   (not if it's imported as a module into another file)
# =============================================================================

if __name__ == "__main__":

    print("=== Creating equipment ===\n")

    # Create instances — each call to ClassName(...) runs __init__
    pump1 = Pump("P-201", "Diffusion Pump 1",    "Bay 3",  flow_rate_lpm=12.5)
    pump2 = Pump("P-202", "DI Water Pump",        "Bay 1",  flow_rate_lpm=8.0)
    temp1 = Sensor("TIC-101", "Furnace Temp",     "Bay 3",  "°C",  800.0, 1100.0)
    flow1 = Sensor("FIC-301", "N2 Flow",          "Bay 3",  "slm", 1.0,   20.0)

    # Create the registry and add everything to it
    registry = EquipmentRegistry()
    registry.add(pump1)
    registry.add(pump2)
    registry.add(temp1)
    registry.add(flow1)

    # -------------------------------------------------------------------------
    print("\n=== Normal operation ===\n")

    pump1.start()
    pump1.add_run_hours(4.5)

    temp1.update(950.0)     # within range → no fault
    flow1.update(15.2)      # within range → no fault

    registry.show_all()

    # -------------------------------------------------------------------------
    print("=== Introducing faults ===\n")

    pump2.set_fault("Inlet pressure low")
    pump2.start()           # should be blocked

    flow1.update(0.3)       # below low limit → auto-fault

    registry.show_faults()

    # -------------------------------------------------------------------------
    print("=== Maintenance work ===\n")

    pump2.log_maintenance("Checked inlet filter — replaced")
    pump2.log_maintenance("Pressure normal after filter change")
    pump2.reset_fault()
    pump2.start()           # should work now

    flow1.update(12.0)      # back in range → auto-clears fault
    flow1.log_maintenance("N2 regulator recalibrated")

    # -------------------------------------------------------------------------
    print("=== Fetching a specific item from the registry ===\n")

    # find() returns the actual object — you can immediately call methods on it
    found = registry.find("TIC-101")
    if found:               # check that find() didn't return None
        print(f"Found: {found.name}, current reading: {found.read():.1f} {found.unit}")
        found.show_log()

    # -------------------------------------------------------------------------
    print()
    flow1.show_log()

    registry.show_all()
    registry.show_faults()