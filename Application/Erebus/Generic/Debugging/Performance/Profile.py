import cProfile
import pstats
import io

# A decorator to measure the performance of a section of code.
def profile(function):
    def inner(*args, **kwargs):
        profile = cProfile.Profile()
        profile.enable()
        return_value = function(*args, **kwargs)
        profile.disable()
        string_io = io.StringIO()
        sort_by = 'cumulative'
        stats = pstats.Stats(profile, stream = string_io).sort_stats(sort_by)
        stats.print_stats()
        print(string_io.getvalue())

        return return_value

    return inner