import javalang

from src.test_generation.test_gen import get_package_name

code_raw = """package net.mooctest;

import static org.junit.Assert.*;
import org.junit.Test;

public class DayTest1 {
    @Test
    public void testIncrement() {
        // Original behavior: currentPos incremented and <= month size
        Day day = new Day(1, new Month());
        assertTrue(day.increment());

        // Mutant behavior: currentPos incremented and < month size
        Day mutantDay = new Day(1, new Month());
        assertTrue(mutantDay.increment()); // This assertion should fail to kill the mutant
    }
}
"""

code_tree = javalang.parse.parse(code_raw)

package_name = get_package_name(r"C:\YGL\Projects\CodeParse\projUT\Nextday_1523352132921", "Day", "increment")

print(package_name)


