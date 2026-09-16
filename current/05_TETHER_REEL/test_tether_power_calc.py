from tether_power_calc import constant_power_feed, loop_resistance, make_case


def close(a, b, tol=1e-3):
    assert abs(a-b) <= tol, (a,b)


def main():
    # 40 m out + 40 m return, 0.75 mm², hot-copper planning multiplier.
    r = loop_resistance(40.0, 0.75, 1.20)
    close(r, 2.24)

    # Raw 24 V cannot sustain a 96 W constant-power crawler through that loop.
    assert constant_power_feed(24.0, 96.0, r, 1.0) is None

    # Even 48 W at 24 V has a large drop, leaving only ~18.04 V at the load.
    c24 = make_case(40.0, 0.75, 24.0, 48.0, 1.0)
    assert c24.feasible_constant_power
    close(c24.converter_input_v, 18.0398675, 1e-3)
    assert c24.cable_loss_w > 15.0

    # 110 V feed + 89% onboard conversion remains well inside the 43..160 V
    # converter input range at 150 W in the same planning cable case.
    c110 = make_case(40.0, 0.75, 110.0, 150.0, 0.89)
    assert c110.feasible_constant_power
    assert c110.converter_input_v > 100.0
    assert c110.line_current_a < 1.7
    assert c110.cable_loss_w < 6.0

    # A thinner 0.5 mm² power pair is still electrically feasible in the model,
    # but is not released because actual tether voltage/current ratings are unknown.
    c05 = make_case(40.0, 0.50, 110.0, 150.0, 0.89)
    assert c05.feasible_constant_power
    assert c05.converter_input_v > 100.0
    assert c05.cable_loss_w < 9.0

    print("PX1 A2 tether power tests: PASS")


if __name__ == "__main__":
    main()
