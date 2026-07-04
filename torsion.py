from manim import *

class Torsion(ThreeDScene):
    def func(self, u, v, t):
        twist = t * (u - (-2)) / 4 # linearly interpolated twist angle from one end to other (t at one end, 0 at other)
        return np.array([np.sin(v + twist), u, np.cos(v + twist)]) # parametric eq for cylinder, each section rotated by its twist amount

    def construct(self):
        self.set_camera_orientation(theta=30 * DEGREES, phi=75 * DEGREES)

        axes = ThreeDAxes()
        twist_angle = ValueTracker(0)
        shear_amount = ValueTracker(0)

        surface = Surface(
            lambda u, v: axes.c2p(*self.func(u, v, twist_angle.get_value())),
            u_range=[-2, 2],
            v_range=[0, TAU],
            resolution=16,
            fill_color=GREEN,
            checkerboard_colors=False,
            stroke_color=WHITE,
            stroke_width=1
        )

         # i think its radius should be 1 but that looked too big and 0.8 fit, idk
        endcap = Circle(0.8, GREEN, fill_opacity=0.9).rotate(PI/2, [1, 0, 0]).move_to(surface.get_critical_point([0, 1, 0]))

        self.play(FadeIn(surface, endcap))

        def make_shear_square(shear):
            square = Square(side_length=1).move_to(UR*0.5) # position the down left corner of the square to origin, so it shears without displacement 
            square.set_stroke(WHITE, 2)
            square.set_fill(GREEN_E, opacity=0.7)
            
            square.apply_matrix(
                np.array(
                    [
                        [1, 0, 0],
                        [shear, 1, 0],
                        [0, 0, 1],
                    ]
                )
            )
            square.shift(2.5*DL)
            
            return square

        shear_square = make_shear_square(shear_amount.get_value())
        self.add_fixed_in_frame_mobjects(shear_square)
        self.remove(shear_square)

        self.play(surface.submobjects[100].animate.set_fill(GREEN_E), FadeIn(shear_square))

        # labels for the shear angle
        gl = DashedLine(shear_square.get_corner(DL), shear_square.get_corner(DL) + RIGHT*1.3)
        ga = Angle(gl, Line(shear_square.get_corner(DL) + [-1, -0.3, 0], shear_square.get_corner(DL)), radius=0.8)
        g = MathTex(r"\gamma").scale(0.7).next_to(ga, RIGHT).shift(UP*0.05)

        self.add_fixed_in_frame_mobjects(gl, ga, g)
        self.remove(gl, ga, g)

        self.play(Create(gl))

        # the arrows and labels for depicting torsioning moments
        carr1 = CurvedArrow(surface.get_edge_center([0, 1, -1]), surface.get_edge_center([1, 1, 0])).shift([0, 0.5, 0]) # the arrow on right end
        carr2 = CurvedArrow(surface.get_edge_center([0, -1, 1]), surface.get_edge_center([1, -1, 0])).shift([0, -0.8, -0.8]) # the arrow on left end
        self.play(FadeIn(carr1, carr2))
        t1 = MathTex("T").rotate(PI/2, [0, 0, 1]).rotate(PI/2, [0, 1, 0]).next_to(carr1, UP)
        t2 = MathTex("T'").rotate(PI/2, [0, 0, 1]).rotate(PI/2, [0, 1, 0]).next_to(carr2, DOWN)
        self.play(Write(t1), Write(t2))

        def f(s):
            s.become(Surface(
                lambda u, v: axes.c2p(*self.func(u, v, twist_angle.get_value())),
                u_range=[-2, 2],
                v_range=[0, TAU],
                resolution=16,
                fill_color=GREEN,
                checkerboard_colors=False,
                stroke_color=WHITE,
                stroke_width=1
            ))
            surface.submobjects[100].set_fill(GREEN_E)
        surface.add_updater(f)

        shear_square.add_updater(lambda sq: sq.become(make_shear_square(shear_amount.get_value())))

        self.play(
            twist_angle.animate.set_value(-PI / 2),
            shear_amount.animate.set_value(0.3), # arbitrary amount that looked close to the element shear angle in the animation
            run_time=4,
        )

        self.play(Create(ga), Write(g))
        
        self.wait(2)

        shear_eq = MathTex(r"\tau = G \cdot \gamma").next_to(gl, UR).shift(RIGHT*0.3)
        self.add_fixed_in_frame_mobjects(shear_eq)
        self.remove(shear_eq)

        self.play(Write(shear_eq))
        self.wait(2)
        self.play(FadeOut(*self.mobjects))


class Relation(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(theta=30 * DEGREES, phi=75 * DEGREES)

        length = 4
        radius_outer = 1
        radius_inner = 0.8
        pos = -3

        outer_cylinder = Cylinder(
            radius=radius_outer,
            height=length,
            checkerboard_colors=False,
            fill_color=GREEN,
            fill_opacity=0.8,
            stroke_color=WHITE,
            stroke_opacity=0.2,
            stroke_width=0,
        ).rotate(PI / 2, axis=RIGHT).shift([0, pos, 0])

        inner_cylinder = Cylinder(
            radius=radius_inner,
            height=length,
            checkerboard_colors=False,
            fill_color=GREEN_E,
            fill_opacity=0.35,
            stroke_width=0,
        ).rotate(PI / 2, axis=RIGHT).shift([0, pos, 0])

        self.play(FadeIn(outer_cylinder))

        outer_rad = Line(outer_cylinder.get_edge_center([0, 1, 0]), outer_cylinder.get_edge_center([0, 1, 1])).set_opacity(0.5)
        outer_rad_label = MathTex("R").scale(0.5).rotate(PI/2, [1, 0, 0]).rotate(PI/1.5, [0, 0, 1]).next_to(outer_rad, LEFT).set_opacity(0.5)
        self.play(Create(outer_rad), Write(outer_rad_label))

        self.play(outer_cylinder.animate.set_opacity(0.2), FadeIn(inner_cylinder))

        # the arrows and labels for depicting torsioning moments
        carr1 = CurvedArrow(outer_cylinder.get_edge_center([0, 1, -1]), outer_cylinder.get_edge_center([-1, 1, 0]), angle=-PI/2, color=GRAY).shift([0, 0.5, 0]) # the arrow on right end
        carr2 = CurvedArrow(outer_cylinder.get_edge_center([0, -1, 1]), outer_cylinder.get_edge_center([1, -1, 0]), angle=PI/2, color=GRAY).shift([0, -0.8, -0.8]) # the arrow on left end
        t1 = MathTex("T", color=GRAY).rotate(PI/2, [0, 0, 1]).rotate(PI/2, [0, 1, 0]).next_to(carr1, UP)
        t2 = MathTex("T'", color=GRAY).rotate(PI/2, [0, 0, 1]).rotate(PI/2, [0, 1, 0]).next_to(carr2, DOWN)
        self.play(FadeIn(carr1, carr2), Write(t1), Write(t2))
    
        phi = ValueTracker(0) #PI/2.8
        
        def create_labels(m=None):
            front_face_center = inner_cylinder.get_critical_point([0, 1, 0])
            arc_p1 = front_face_center + radius_inner*np.array([np.cos(phi.get_value()), 0, np.sin(phi.get_value())])
            arc_p2 = inner_cylinder.get_edge_center([1, 1, 0])
            arc = ArcBetweenPoints(arc_p1, arc_p2, stroke_color=ORANGE)
            rad = Line(front_face_center, arc_p2)
            rot_rad = Line(front_face_center, arc_p1)
            long = Line(arc_p2, inner_cylinder.get_edge_center([1, -1, 0]))

            long_line = ParametricFunction(lambda t: np.array([radius_inner * np.cos(phi.get_value()*t), length * t, radius_inner * np.sin(phi.get_value()*t)])).shift([0, pos - length/2, 0])
            l = VGroup(arc, rad, rot_rad, long, long_line)
            if m:
                m.become(l)
            else:
                return l

        labels = create_labels()
        labels.add_updater(create_labels)

        self.play(Create(labels))
        self.play(phi.animate.set_value(PI/2.8), rate_func=linear)
        self.wait()

        labelL = MathTex("L").scale(0.8).rotate(PI/2, [1, 0, 0]).rotate(PI/2, [0, 0, 1]).next_to(labels[3], RIGHT).shift([0, 0, -0.2])
        labelR = MathTex(r"\rho").scale(0.8).rotate(PI/2, [1, 0, 0]).rotate(PI/1.5, [0, 0, 1]).next_to(labels[1], 0.5*IN)
        labelPhi = MathTex(r"\phi").scale(0.7).rotate(PI/2, [1, 0, 0]).rotate(PI/1.5, [0, 0, 1]).next_to(labels[2], 0.1*RIGHT)
        self.play(Write(labelL), Write(labelR), Write(labelPhi))

        carr = CurvedArrow(outer_cylinder.get_edge_center([-1, 0, 1]), outer_cylinder.get_edge_center([-1, 0, 1]) + (UP + 0.5*OUT)*3, angle=-0.6*PI)
        self.play(FadeIn(carr))

        projection = Rectangle(width=4, height=1.6 * PI, fill_color=GREEN_E, fill_opacity=0.5, stroke_width=1).scale(0.7)
        projection.to_corner(UR).shift(DOWN*0.1 + LEFT*2)

        pw = Brace(projection, DOWN)
        ph = Brace(projection, LEFT)

        pwl = MathTex("L").scale(0.7).next_to(pw, DOWN)
        phl = MathTex(r"2 \pi \rho").scale(0.7).next_to(ph, LEFT)

        pl1 = Line(projection.get_edge_center(LEFT), projection.get_edge_center(RIGHT))
        pl2 = Line(projection.get_edge_center(LEFT), projection.get_edge_center(RIGHT) + UP*0.8)
        pl3 = Line(pl1.get_end(), pl2.get_end(), color=ORANGE)

        pg = Angle(pl1, pl2, radius=1.5)
        gamma = MathTex(r"\gamma").scale(0.7).next_to(pg, RIGHT)

        plg = MathTex(r"L \cdot \gamma", color=ORANGE).scale(0.8).next_to(pl3, RIGHT)

        psector = Sector(radius=0.8, start_angle=PI, angle=-phi.get_value(), fill_color=GREEN_E, fill_opacity=0.5, stroke_width=2).to_corner(RIGHT)
        psarc = Arc(radius=0.8, start_angle=PI, angle=-phi.get_value(), arc_center=psector.get_arc_center(), stroke_color=ORANGE, stroke_width=4)
        pphi = MathTex(r"\phi").scale(0.7).next_to(psarc).shift(LEFT*0.35 + DOWN*0.1)
        prho = MathTex(r"\rho").scale(0.7).next_to(psector, DOWN)

        ppr = MathTex(r"\rho \cdot \phi", color=ORANGE).scale(0.8).next_to(psarc, LEFT, buff=0).shift(UP*0.2)

        pfin = MathTex(r"L \cdot \gamma = \rho \cdot \phi", color=ORANGE).scale(1.5).next_to(projection, DOWN).shift(DOWN*1.5)

        self.add_fixed_in_frame_mobjects(projection, pw, ph, pwl, phl, pl1, pl2, pl3, pg, gamma, plg, psector, psarc, pphi, prho, ppr, pfin)
        self.remove(projection, pw, ph, pwl, phl, pl1, pl2, pl3, pg, gamma, plg, psector, psarc, pphi, prho, ppr, pfin)

        self.play(FadeIn(projection, pw, ph), Write(pwl), Write(phl))
        self.wait()
        self.play(Create(pl1), Create(pl2), Create(pl3))
        self.play(Create(pg), Write(gamma))
        self.play(Write(plg))
        self.wait()

        self.play(FadeIn(psector, psarc))
        self.play(Write(pphi), Write(prho))
        self.play(Write(ppr))
        self.wait(3)
        self.play(Write(pfin))
        self.wait(2)