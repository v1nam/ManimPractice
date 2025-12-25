from manim import *

class Practice(Scene):
    def construct(self):
        cl = Rectangle(height=0.5, width=4, fill_opacity=0, stroke_color=BLUE)
        t, b = cl.get_critical_point(UL)+UP, cl.get_critical_point(DL)+DOWN
        line = Line(t, b)

        n = 10
        fixture = VGroup(*[Line(t + (b - t) * i / n, t + (b - t) * (i+1) / n + LEFT*0.2).set_color(GRAY) for i in range(n)])
        l = BraceLabel(cl, "L", UP)
        self.play(Create(fixture), DrawBorderThenFill(cl), DrawBorderThenFill(line), FadeIn(l))
        def t(point):
            x, y, z = point
            x = x + 2
            y -= (0.05/24)*x**2*(12-x)
            x = x - 2
            return np.array([x, y, z])
        clb = cl.copy().set_opacity(0.4).set_stroke(BLUE_B).set_fill(BLUE_C)
        self.play(FadeIn(clb, run_time=0.5))
        self.play(FadeOut(l))

        arr = Arrow(start=cl.get_critical_point(UR)+UP, end=cl.get_critical_point(UR), color=RED, buff=0.1)
        f = VGroup(arr, Tex("P", color=RED, font_size=30).next_to(arr, UL, buff=0.1))

        self.play(ApplyPointwiseFunction(t, clb),
                  Create(f))
        self.wait()