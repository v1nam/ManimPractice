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

         # i think its radius should be 1 but that looked too big and 0.9 fit, idk
        endcap = Circle(0.8, GREEN, fill_opacity=0.9).rotate(PI/2, [1, 0, 0]).move_to(surface.get_critical_point([0, 1, 0]))

        self.play(FadeIn(surface, endcap))
        self.play(surface.submobjects[100].animate.set_fill(GREEN_E))

        # the arrows and labels for depicting torsioning moments
        carr1 = CurvedArrow(surface.get_edge_center([0, 1, -1]), surface.get_edge_center([1, 1, 0])).shift([0, 0.5, 0]) # the arrow on right end
        carr2 = CurvedArrow(surface.get_edge_center([0, -1, 1]), surface.get_edge_center([1, -1, 0])).shift([0, -0.8, -0.8]) # the arrow on left end
        self.play(FadeIn(carr1, carr2))
        t1 = MathTex("T").rotate(PI/2, [0, 0, 1]).rotate(PI/2, [0, 1, 0]).next_to(carr1, UP)
        t2 = MathTex("T'").rotate(PI/2, [0, 0, 1]).rotate(PI/2, [0, 1, 0]).next_to(carr2, DOWN)
        self.play(Write(t1), Write(t2))

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

        self.play(FadeIn(shear_square))

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

        # labels for the shear angle
        gl = DashedLine(shear_square.get_corner(DL), shear_square.get_corner(DL) + RIGHT*1.3)
        ga = Angle(gl, Line(shear_square.get_corner(DL) + [-1, -0.3, 0], shear_square.get_corner(DL)), radius=0.8)
        g = MathTex(r"\gamma").scale(0.7).next_to(ga, RIGHT).shift(UP*0.05)

        self.add_fixed_in_frame_mobjects(gl, ga, g)
        self.remove(gl, ga, g)

        self.play(Create(gl))
         
        self.play(
            twist_angle.animate.set_value(-PI / 2),
            shear_amount.animate.set_value(0.3), # arbitrary amount that looked close to the element shear angle in the animation
            run_time=4,
        )

        self.play(Create(ga), Write(g))
        
        self.wait(2)