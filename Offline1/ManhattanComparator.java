import java.util.Comparator;
import java.util.HashMap;

import static java.lang.Math.abs;

public class ManhattanComparator implements Comparator<search_node> {

    public int compare(search_node s1, search_node s2) {
        int h1 = manhattan_distance(s1.getBoard(), s1.getBoard().length);
        int h2 = manhattan_distance(s2.getBoard(), s2.getBoard().length);
        if ( ( s1.getMoves() + h1 ) > ( s2.getMoves() + h2 ) )
            return 1;
        else if ( ( s1.getMoves() + h1 ) < ( s2.getMoves() + h2) )
            return -1;
        return 0;
    }


    public static int manhattan_distance(String[][] arr, int k){
        int total = 0;
        int value;
        for( int i = 0 ; i < k ; i++ ){
            for( int j = 0 ; j < k ; j++ ){
                if( arr[i][j].equalsIgnoreCase("*") ){
                    continue;
                }
                value = Integer.parseInt(arr[i][j]);
                Pair pair = main.ideal.get(value);
                int row_diff = abs(pair.getRow() - i);
                int column_diff = abs(pair.getColumn() - j);
                total += row_diff + column_diff;
            }
        }
        return total;
    }
}
