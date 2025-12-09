#from setuptools import setup, Extension
#from setuptools import Extension
from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize, build_ext
import Cython.Compiler.Options
Cython.Compiler.Options.annotate = True

extensions = [
    #Extension("anim_sprite_cy", ['anim_sprite_cy.pyx']),
    #Extension("anim_sprite_cy", ['anim_sprite.py']),
    #Extension('falling_line_cy', ['falling_line.py']),
    #Extension('fps_counter_cy', ['fps_counter.py'], depends=["anim_sprite_cy"]),
    # Extension('../spritelib', [
    #     'spritelib/anim_sprite.py',
    #     'spritelib/falling_line.py',
    #     'spritelib/fps_counter.py',
    #     ],
    #     language="c++",
    #     #extra_compile_args=["-std=c++11"]
    #     )
    Extension("spritelib_cy.anim_sprite", ['spritelib_cy/anim_sprite.py'], language="c++", include_dirs=[".", "./spritelib_cy/"]),
    Extension("spritelib_cy.falling_line", ['spritelib_cy/falling_line.py'], language="c++", include_dirs=[".", "./spritelib_cy/"]),
    Extension("spritelib_cy.fps_counter", ['spritelib_cy/fps_counter.py'], language="c++", include_dirs=[".", "./spritelib_cy/"]),
    ]

setup (
    #name="spritelib",
    version="1.0.0",
    python_requires=">=3.7",
    description="Matrix Sprite Library",
    #package_dir={"": "spritelib"},
    #packages=['spritelib', 'spritelib.anim_sprite', 'spritelib.falling_line', 'spritelib.fps_counter'],
    #namespace_packages=['spritelib_cy'],
    ext_modules=cythonize(extensions, force=True, compiler_directives={"language_level": 3}, language_level=3),
    zip_safe=False
)