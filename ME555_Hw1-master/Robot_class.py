class robot:
    def __init__(self, Vrx, Vry, Pr, drr, drt, drb, Wrt, label, frt, frr, Frt, Frr, Frb, w_rt, w_rr, N_t):
        self.Vrx = Vrx  #velocity at x
        self.Vry = Vry  #velocity at y
        self.Pr = Pr
        self.drr = drr
        self.drt = drt
        self.drb = drb
        self.Wrt = Wrt
        self.label = label
        self.frt = frt  #frt = [(frtx,frty,label),(...),(...)]
        self.frr = frr  #frr = [(frrx,frry,label),(...),(...)]
        self.Frt = Frt
        self.Frr = Frr
        self.Frb = Frb
        self.wrt = w_rt
        self.wrr = w_rr
        self.N_t = N_t
class target:
    def __init__(self, Vtx, Vty, Pt, dtb, label, Ftb, dtt):
        self.Vtx = Vtx
        self.Vty = Vty
        self.Pt = Pt
        self.dtb = dtb
        self.label = label
        self.Ftb = Ftb
        self.dtt = dtt