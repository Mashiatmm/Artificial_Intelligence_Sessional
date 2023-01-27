import java.util.Comparator;
import java.util.Scanner;

public class LinearComparator extends ManhattanComparator implements Comparator<search_node> {
    public int compare(search_node s1, search_node s2) {
        int h1 = linear_distance(s1.getBoard(), s1.getBoard().length);
        int h2 = linear_distance(s2.getBoard(), s2.getBoard().length);
        if ((s1.getMoves() + h1) > (s2.getMoves() + h2)) return 1;
        else if ((s1.getMoves() + h1) < (s2.getMoves() + h2)) return -1;
        return 0;
    }

    public static int linear_distance(String[][] arr, int k) {
        // measure row conflict
        int total = manhattan_distance(arr, k);
        int value, later_value;
        Pair pair;
        for (int i = 0; i < k; i++) {
            for (int j = 0; j < k; j++) {
                if (arr[i][j].equalsIgnoreCase("*")) {
                    continue;
                }
                value = Integer.parseInt(arr[i][j]);
                pair = main.ideal.get(value);
                if( pair.getRow() != i){
                    // element not in right column
                    continue;
                }
                // check for linear conflict
                for( int l = j + 1 ; l < k ; l++ ){
                    if (arr[i][l].equalsIgnoreCase("*")) {
                        continue;
                    }
                    later_value = Integer.parseInt(arr[i][l]);
                    pair = main.ideal.get(later_value);
                    if( (later_value < value) && ( pair.getRow() == i ) ){
                        total += 2;
                    }
                }
            }
        }
        return total;
    }


//        public static void main(String[] args){
//        Scanner sc = new Scanner(System.in);
//        int k; // grid size
//        System.out.println(" Enter the value of k : ");
//        while(true){
//            try{
//                k = Integer.parseInt( sc.nextLine() );
//                break;
//            }
//            catch( Exception e ){
//                System.out.println("Not an Integer. Enter again");
//            }
//        }
//
//        // store ideal output
//        main.store_ideal(k);
//        String[][] arr = new String[k][k];
//        System.out.println("Input of the Initial Board : ");
//        for(int i = 0 ; i < k ; i++ ){
//            for(int j = 0 ; j < k ; j++ ){
//                arr[i][j] = sc.nextLine();
//            }
//        }
//
//        System.out.println(linear_distance(arr, k));
//    }
}
