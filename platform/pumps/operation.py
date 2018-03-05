import PWM_Pump as pump

a = pump.Pump("gpio2")
b = pump.Pump("gpio3")
c = pump.Pump("gpio4")
nitrate = pump.Pump("gpio5")
base = pump.Pump("gpio6")
waste = pump.Pump("gpio7")
wash = pump.Pump("gpio8")
stir = pump.Pump("gpio9")


def disp(pump, volume): # insert pump and volume you want to dispense in ml

    cal ={'a' : 4.4, 'b' : 4.0, 'c' : 4.1, 'nitrate' : 4.2, 'base':4.3, 'waste': 4.2, 'wash':4.0}

    if pump == 'a':
        a.run(volume/(cal['a']/60))
    elif pump == 'b':
        b.run(volume/(cal['b']/60))
    elif pump == 'c':
        c.run(volume/(cal['c']/60))
    elif pump == 'nitrate':
        nitrate.run(volume/(cal['nitrate']/60))
    elif pump == 'base':
        base.run(volume/(cal['base']/60))
    elif pump == 'waste':
        waste.run(volume/(cal['waste']/60))
    elif pump == 'wash':
        wash.run(volume/(cal['wash']/60))


def cln_cycle():
    print ("Start Cleaning Cycle")
    disp('waste', 10)
    disp('wash', 3)
    disp('waste', 4)
    print ("End of Cleaning Cycle")

def dirty_clean(counter):
    print('Running dirty cleaning cycle')
    if counter == 0:
        disp('waste', 5)
    else:
        disp('waste', 6)
    print('End dirty cleaning cycle')
    


def prime_pumps():
    print ('priming pumps')
    waste.on()
    a.run(5)
    b.run(5)
    c.run(5)
    nitrate.run(5)
    base.run(5)
    waste.run(30)
    disp('wash',2)
    disp('waste',2.5)
    disp('wash',2)
    disp('waste',2.5)
