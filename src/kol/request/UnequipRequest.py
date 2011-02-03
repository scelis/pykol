from GenericRequest import GenericRequest

class UnequipRequest(GenericRequest):
    """
    Unequips the equipment in the designated slot.  HAT, WEAPON, OFFHAND,
    SHIRT, PANTS, SLOT1, SLOT2, SLOT3, and FAMILIAR may be used to de-equip
    certain things, or ALL will de-equip everything.
    """

    HAT = "hat"
    WEAPON = "weapon"
    OFFHAND = "offhand"
    SHIRT = "shirt"
    PANTS = "pants"
    SLOT1 = "acc1"
    SLOT2 = "acc2"
    SLOT3 = "acc3"
    FAMILIAR = "familiarequip"
    ALL = 999

    def __init__(self, session, slot):
        super(UnequipRequest, self).__init__(session)

        if slot == self.ALL:
            self.url = session.serverURL + "inv_equip.php?pwd=" + str(session.pwd) + "&action=unequipall"
        else:
            self.url = session.serverURL + "inv_equip.php?pwd=" + str(session.pwd) + "&action=unequip&type=" + slot

