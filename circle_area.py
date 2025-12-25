from manim import *

class CreateCircle(Scene):
    def construct(self):
        radius_line = Line(start=ORIGIN, end=RIGHT, color=BLUE)
        radius_label = Tex("R", font_size=30).next_to(radius_line, UP)
        circle = Circle(1, stroke_color=BLUE, fill_opacity=0)
        self.play(Create(radius_line), Write(radius_label))
        self.play(Create(circle))
        self.wait()
        self.play(FadeOut(radius_label, radius_line))

        n = 20
        sectors = VGroup(*(Sector(angle=2*PI/n, start_angle=s*(2*PI/n), color=BLUE, fill_opacity=0.5, stroke_width=1) for s in range(n)))
        rect = self.create_rect(n)

        self.play(Create(sectors), FadeOut(circle))

        self.play(sectors.animate.move_to(3*LEFT))
        self.wait()

        self.play(Transform(sectors, rect))
        self.wait(0.5)

        self.play(Transform(sectors, self.create_rect(50)))
        self.play(Transform(sectors, self.create_rect(150)))
        self.play(Transform(sectors, self.create_rect(500)))

        breadth = BraceLabel(sectors, "R", LEFT, font_size=30)
        length = BraceLabel(sectors, "\pi R", UP, font_size=30)
        self.play(FadeIn(breadth, length))
        self.wait()

        area = MathTex(r"Area = \pi R \cdot R", font_size = 40).next_to(sectors, DOWN * 2)
        self.play(Write(area))
        self.play(Transform(area, MathTex(r"Area = \pi R^2", font_size = 40).next_to(sectors, DOWN * 2)))
        self.wait()
        self.play(FadeOut(sectors, breadth, length))
        self.play(Create(circle), area.animate.shift(DOWN))
        circle.set_fill(BLUE)
        self.play(circle.animate.set_opacity(0.5))
        self.wait()

    
    @staticmethod
    def create_rect(n):
        rect = VGroup(*(Sector(angle=2*PI/n, start_angle=s*(2*PI/n), stroke_width=1, fill_opacity=0.5, color=BLUE) for s in range(n)))
        for i, s in enumerate(rect):
            s.rotate(-i*2*PI/n)
            if i % 2 == 0:
                s.rotate(-(PI*(1/2 + 1/n)))
                s.move_to(i*PI/n*RIGHT)
            else:
                s.rotate(PI*(1/2 - 1/n))
                s.move_to(i*PI/n*RIGHT)
        rect.move_to(ORIGIN)
        return rect
