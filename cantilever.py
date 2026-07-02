from manim import *
import math

class Cantilever(Scene):
    # Fixed wall symbol at the left end of the beam.
    @staticmethod
    def fixed_wall_symbol(anchor_point, height):
        ex = 1.2*height/2
        wall_line = Line(
            anchor_point + ex * DOWN,
            anchor_point + ex * UP,
            color=GRAY,
            stroke_width=5,
        )
        hatches = VGroup()
        for offset in np.linspace(-height/2, height/2, 6):
            hatch_start = anchor_point + offset * UP
            hatch_end = hatch_start + np.array([-height/6, -height/6, 0])
            hatches.add(Line(hatch_start, hatch_end, color=GRAY_B, stroke_width=1))

        return VGroup(wall_line, hatches)

    def construct(self):
        # Main 2D cantilever beam as a rectangle.
        beam = Rectangle(width=10, height=1.0, color=BLUE_B, fill_opacity=0.15)
        beam.move_to(UP * 2)

        wall = self.fixed_wall_symbol(beam.get_left(), beam.height)
        cantilever = VGroup(beam, wall)
        self.play(DrawBorderThenFill(cantilever))
        self.wait(0.25)

        # Small element of the beam to zoom into.
        dx_slice = Rectangle(width=0.4, height=1.0, color=YELLOW)
        dx_slice.move_to(beam.get_center() + 3.4 * RIGHT)
        dx_label = MathTex("dx").next_to(dx_slice.get_bottom(), DOWN, buff=0.1)

        self.play(FadeIn(dx_slice), dx_slice.animate.set_fill(YELLOW, opacity=0.2).set_stroke(width=0), Write(dx_label))
        self.wait()

        # Zoomed section shown below.
        w, h = 5, 2
        section = Rectangle(width=w, height=h, color=WHITE)
        self.play(FadeOut(cantilever, dx_label), Transform(dx_slice, section))
        br = Brace(section)
        self.play(FadeIn(br, dx_label.next_to(br, DOWN)))
        self.wait()

        # centerline or neutral surface of beam
        self.play(FadeOut(br, dx_label))
        center_line = DashedLine(section.get_left(), section.get_right(), dash_length=0.12, color=GREEN)
        a_label = MathTex("A").next_to(center_line.get_start(), LEFT, buff=0.15)
        b_label = MathTex("B").next_to(center_line.get_end(), RIGHT, buff=0.15)
        self.play(Create(center_line), Write(a_label), Write(b_label))

        # Arbitrary line CD above centerline.
        y_offset = 0.6
        upper_line = Line(section.get_left() + y_offset * UP, section.get_right() + y_offset * UP, color=ORANGE)
        c_label = MathTex("C").next_to(upper_line.get_start(), LEFT, buff=0.15)
        d_label = MathTex("D").next_to(upper_line.get_end(), RIGHT, buff=0.15)
        self.play(Create(upper_line), Write(c_label), Write(d_label))

        # Distance y between AB and CD.

        y_marker = DoubleArrow(
            start=center_line.get_center(),
            end=upper_line.get_center(),
            buff=0)

        y_label = MathTex("y").next_to(y_marker, LEFT, buff=0.1)

        self.play(FadeIn(y_marker), Write(y_label))
        self.wait()

        beam_section = VGroup(section, upper_line, center_line, a_label, b_label, c_label, d_label, y_marker, y_label)
        self.remove(dx_slice)
        self.play(beam_section.animate.to_corner(DR))

        start_angle = PI / 2 - (5/6)
        arc_theta = 10 / 6
        curved_section = AnnularSector(inner_radius=2, outer_radius=4, angle=arc_theta, start_angle=start_angle, fill_opacity=0, stroke_width=4).shift(DOWN)
        r = 10000
        sec_copy = AnnularSector(inner_radius=r, outer_radius=r + h, angle=(w/r), start_angle=(PI/2 - 0.5*(w/r)), fill_opacity=0, stroke_width=4).shift(DOWN * (r + h) * 0.5).move_to(section)

        moment_arrow1 = CurvedArrow(curved_section.get_corner(DL), curved_section.get_corner(DL)+DR).scale(0.5)
        moment_label1 = MathTex("M").next_to(moment_arrow1, DL, buff=0.05).scale(0.8)
        moment_arrow2 = CurvedArrow(curved_section.get_corner(DR), curved_section.get_corner(DR)+DL, angle=-PI/4).scale(0.5)
        moment_label2 = MathTex("M").next_to(moment_arrow2, DR, buff=0.05).scale(0.8)
        moment_group = VGroup(moment_arrow1, moment_arrow2, moment_label1, moment_label2)
        self.play(ReplacementTransform(sec_copy, curved_section),
                  FadeIn(moment_group))

        center_line_c = Arc(3, start_angle=start_angle, angle=arc_theta, color=GREEN).shift(DOWN)
        upper_line_c = Arc(3 + y_offset, start_angle=start_angle, angle=arc_theta, color=ORANGE).shift(DOWN)

        ac_label = MathTex("A'").next_to(center_line_c.get_end(), LEFT, buff=0.2)
        bc_label = MathTex("B'").next_to(center_line_c.get_start(), RIGHT, buff=0.2)

        cc_label = MathTex("C'").next_to(upper_line_c.get_end(), LEFT, buff=0.2)
        dc_label = MathTex("D'").next_to(upper_line_c.get_start(), RIGHT, buff=0.2)
        
        center_line_c = DashedVMobject(center_line_c, dashed_ratio=0.5)

        self.play(Create(center_line_c), Write(ac_label), Write(bc_label))
        self.play(Create(upper_line_c), Write(cc_label), Write(dc_label))
        self.wait()

        radius_arrow = Arrow(start=ORIGIN, end=UP*3, stroke_width=2, max_tip_length_to_length_ratio=0.09, color=ManimColor((0.8, 0.8, 0.8)), buff=0.02).shift(DOWN)
        radius_label = MathTex("R").next_to(radius_arrow, RIGHT, buff=0.1)
        y_marker_c = DoubleArrow(
            start=UP*3,
            end=UP*(3 + y_offset),
            buff=0).shift(DOWN)

        y_label_c = MathTex("y").next_to(y_marker_c, LEFT, buff=0.1)
        self.play(Create(y_marker_c), Write(y_label_c))
        self.play(GrowArrow(radius_arrow), Write(radius_label))
        l1 = Line(ORIGIN, [2*math.sin(arc_theta/2), 2*math.cos(arc_theta/2), 0], color=GRAY, stroke_width=2).shift(DOWN)
        l2 = Line(ORIGIN, [-2*math.sin(arc_theta/2), 2*math.cos(arc_theta/2), 0], color=GRAY, stroke_width=2).shift(DOWN)
        theta_label_arc = Angle(l1, l2, radius=0.4, color=GRAY)
        theta_label = MathTex(r"\theta").next_to(theta_label_arc, DL, buff=0.1)
        theta_group = VGroup(l1, l2, theta_label_arc)
        self.play(Create(theta_group), Write(theta_label))
        self.wait()

        curved_beam = VGroup(curved_section, moment_group, center_line_c, upper_line_c, ac_label, bc_label, cc_label, dc_label, radius_arrow, radius_label, theta_label, theta_group, y_label_c, y_marker_c)
        self.play(curved_beam.animate.to_corner(DL))
        self.wait(2)

        t = Tex("strain in ", "CD", r" $=$ ", r"$\frac{\text{change in length}}{\text{original length}}$")
        t[1].set_color(ORANGE)
        t.to_edge(UP)
        self.play(Write(t))
        t1 = MathTex(r"{\epsilon}_{CD} = \frac{C'D' - CD}{CD}").to_edge(UP)
        # self.add(index_labels(t2[0]))
        self.play(TransformMatchingTex(t, t1))
        self.wait()
        
        t_n = Tex(r"But $CD = AB$ and $AB = A'B'$ (neutral axis)").scale(0.7).next_to(beam_section, UP, buff=1)

        t_n[0][3:5].set_color(ORANGE) # color of CD
        for t_c in (t_n[0][6:8], t_n[0][11:13], t_n[0][14:18]):
            t_c.set_color(GREEN) # color of AB, A'B'

        self.play(Write(t_n))
        self.wait()
        t2 = MathTex(r"{\epsilon}_{CD} = \frac{C'D' - A'B'}{A'B'}").to_edge(UP)
        
        self.play(TransformMatchingTex(t1, t2))
        self.wait()
        self.play(FadeOut(t_n))
        self.wait()
        t3 = MathTex(r"{\epsilon}_{CD} = \frac{(R+y)\theta - R\theta}{R\theta}").to_edge(UP)
        self.play(TransformMatchingTex(t2, t3))
        self.wait()
        t4 = MathTex(r"{\epsilon}_{CD} = \frac{R\theta+y\theta - R\theta}{R\theta}").to_edge(UP) 
        self.play(TransformMatchingTex(t3, t4))
        t5 = MathTex(r"{\epsilon}_{CD} = \frac{y}{R}").to_edge(UP)
        self.play(TransformMatchingTex(t4, t5))
        self.wait(2)
        ts = Tex(r"Now, $\frac{\text{stress}}{\text{strain}} = E$ \\ Where $E$ is Young's Modulus").next_to(t5, DOWN)
        self.play(Write(ts))
        self.wait()
        ts1 = MathTex(r"\frac{\sigma}{ {\epsilon}_{CD} } = E").move_to(ts)
        ts2 = MathTex(r"\sigma = {\epsilon}_{CD} \cdot E").move_to(ts1)
        self.play(TransformMatchingTex(ts, ts1))
        self.play(TransformMatchingTex(ts1, ts2))
        self.wait()
        ts3 = MathTex(r"\sigma = \frac{y}{R} \cdot E").move_to(ts2)
        self.play(TransformMatchingTex(ts2, ts3))
        self.play(FadeOut(t5), ts3.animate.to_edge(UP))
        self.play(Circumscribe(ts3, fade_out=True, run_time=2))
        self.wait()
        self.play(FadeOut(beam_section, curved_beam, ts3))

class Beam3D(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=60 * DEGREES, theta=60 * DEGREES)
        
        beam = Prism(dimensions=[2, 5, 2], fill_opacity=0, stroke_width=4, color=GRAY_D)
        self.play(FadeIn(beam), run_time=2)

        centerline = DashedLine(beam.get_edge_center([1, -1, 0]), beam.get_edge_center([1, 1, 0]), color=GREEN)
        self.play(Create(centerline), run_time=0.5)
        label_c = Tex("C", color=GREEN).rotate(PI/2, OUT).rotate(PI/2, UP).next_to(centerline.get_start(), DOWN)
        label_d = Tex("D", color=GREEN).rotate(PI/2, OUT).rotate(PI/2, UP).next_to(centerline.get_end(), UP)
        self.play(Write(label_c), Write(label_d))

        element = Square(0.2, color=YELLOW).set_fill(YELLOW, opacity=0.4).move_to(beam.get_edge_center(UP)).rotate(PI/2, RIGHT).shift([-0.3, 0, 0.6])
        self.play(FadeIn(element))
        cross_section_line = DashedLine(beam.get_edge_center([1, 1, 0]), beam.get_edge_center([-1, 1, 0]), color=PURPLE)
        dA = MathTex(r"\delta A", color=YELLOW).scale(0.7).next_to(element, LEFT + OUT, buff=0.1).rotate(PI/2, RIGHT).flip(OUT)
        self.play(Write(dA))
        self.play(Create(cross_section_line), run_time=0.5)

        force_arrow = Arrow(element.get_center(), element.get_center() + UP*2, buff=0)
        force_text = Tex("F").next_to(force_arrow.get_end(), UP).rotate(PI/2, RIGHT).flip(OUT)
        self.play(GrowArrow(force_arrow))
        self.play(Write(force_text))

        vertical = DashedLine(element.get_center(), element.get_center() + IN * 0.6)
        vertical_y = Tex("y").scale(0.7).next_to(vertical, buff=0.1).rotate(PI/2, RIGHT).flip(OUT)
        self.play(Create(vertical), Write(vertical_y), run_time=0.5)

        eq1 = MathTex(r"F = ", r"\sigma", r"\cdot \delta A")
        eq2 = MathTex(r"F = ", r"\frac{Ey}{R}", r"\cdot \delta A")
        self.add_fixed_in_frame_mobjects(eq1, eq2)
        self.remove(eq1, eq2)

        eq1 = eq1.to_edge(LEFT)
        eq2 = eq2.to_edge(LEFT)

        self.play(Write(eq1))
        self.wait()
        self.play(FadeOut(eq1), FadeIn(eq2))
        self.wait()

        eq3 = MathTex(r"M_F = ", r"F \cdot y")
        eq4 = MathTex(r"M_F = ", r"\frac{Ey}{R} \delta A", r"\cdot y")
        eq5 = MathTex(r"M_F = ", r"\frac{E}{R} y^2 \delta A")

        self.add_fixed_in_frame_mobjects(eq3, eq4, eq5)
        self.remove(eq3, eq4, eq5)
        eq3 = eq3.next_to(eq2, DOWN, buff=1)
        eq4 = eq4.move_to(eq3)
        eq5 = eq5.move_to(eq4)
        self.play(Write(eq3))
        self.wait()
        self.play(FadeOut(eq3), FadeIn(eq4))
        self.play(FadeOut(eq4), FadeIn(eq5))
        self.wait()
        self.play(eq5.animate.move_to(eq2), FadeOut(eq2))
        eq6 = MathTex(r"M = ", r"\frac{E}{R}", r"\sum y^2 \delta A").move_to(eq5)
        ar = Arrow(eq6[2].get_edge_center(DOWN), eq6[2].get_edge_center(DOWN) + DOWN)
        label = Tex("Second moment of area (I)").scale(0.7).next_to(ar, DOWN)
        self.add_fixed_in_frame_mobjects(eq6, ar, label)
        self.remove(eq6, ar, label)
        self.play(FadeOut(eq5), FadeIn(eq6))
        self.play(GrowArrow(ar))
        self.play(Write(label))
        self.wait()
        self.play(FadeOut(ar, label))
        eq = MathTex(r"M = \frac{E}{R} \cdot", r"I").move_to(eq6)
        self.add_fixed_in_frame_mobjects(eq)
        self.remove(eq)

        self.play(FadeOut(eq6), FadeIn(eq))
        

        self.wait(2)

class Deflection(Scene):
    def construct(self):
        beam = Rectangle(width=10, height=1.0, color=BLUE_B, fill_opacity=0.15)
        wall = Cantilever.fixed_wall_symbol(beam.get_left(), beam.height)
        cantilever = VGroup(beam, wall)
        self.play(DrawBorderThenFill(cantilever))
        cline = Line(beam.get_left(), beam.get_right())
        farr = Arrow(beam.get_corner(UR) + 1.5*UP, beam.get_corner(UR))
        f = Tex("F").next_to(farr, RIGHT)
        self.play(Create(cline), GrowArrow(farr), Write(f))
        self.wait(2)
        

