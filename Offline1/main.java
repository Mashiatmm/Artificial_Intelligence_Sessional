import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.util.*;

public class main {
    public static HashMap<Integer, Pair> ideal = new HashMap<Integer, Pair>();

    public static PriorityQueue<search_node> open_list_1 = new
            PriorityQueue<search_node>( new HammingComparator() );
    public static PriorityQueue<search_node> open_list_2 = new
            PriorityQueue<search_node>( new ManhattanComparator() );
    public static PriorityQueue<search_node> open_list_3 = new
            PriorityQueue<search_node>( new LinearComparator() );

    public static HashMap<String, search_node> close_list = new HashMap<>();

    public static void store_ideal(int k){
        int value;
        for(int i = 0 ; i < k ; i++ ){
            for( int j = 0 ; j < k ; j++ ){
                value = i*k + j + 1;
                Pair pair = new Pair(i, j);
                ideal.put(value, pair);
            }
        }
    }

    public static boolean checked(search_node temp){
        return close_list.containsKey(temp.toString());

    }

    public static void print_boards(search_node sn){
        if (sn.getPrev_search_node() != null){
            print_boards(sn.getPrev_search_node());
        }
        String[][] temp = sn.getBoard();
        int length = temp.length;
        for( int i = 0 ; i < length ; i++ ){
            for( int j = 0 ; j < length ; j++ ){
                System.out.print(temp[i][j] + " ");
            }
            System.out.println();
        }
        System.out.println();
    }

    public static int get_inversions(String[][] arr, int k){
        int[] temp_array = new int[k*k - 1];
        int idx = 0;
        // 1d array
        for(int i = 0 ; i < k ; i++){
            for( int j = 0 ; j < k ; j++){
                if(arr[i][j].equalsIgnoreCase("*")){
                    continue;
                }
                temp_array[idx] = Integer.parseInt(arr[i][j]);
                idx++;
            }
        }
        // count inversions
        int inv = 0;
        for(int i = 0 ; i < temp_array.length - 1 ; i++){
            for( int j = i+1 ; j < temp_array.length ; j++){
                if( temp_array[i] > temp_array[j] ){
                    inv++;
                }
            }
        }
        return inv;
    }

    public static boolean check_solvability(String[][] arr, int k){
        int inv = get_inversions(arr, k);

        if( ( k % 2 ) == 0){
            // get blank's coordinates
            int row = 0 ;
            for( int i = 0 ; i < k ; i++ ){
                for( int j = 0 ; j < k ; j++ ){
                    if( arr[i][j].equalsIgnoreCase("*") ){
                        row = i;
                        break;
                    }
                }
            }
            // blank on even row from bottom and number of inversions odd
            // blank on odd row from bottom and number of inversions even
            int check = (k - row + inv) & 1;
            if(check == 1) return true;
            else return false;
        }
        else{
            if(inv % 2 == 1) return false;
            else return true;
        }



    }

    public static PriorityQueue<search_node> get_neighbours(PriorityQueue<search_node> pq, search_node curr_node, int k){
        String[][] arr = curr_node.getBoard();
        int row = 0 ;
        int column = 0;
        for( int i = 0 ; i < k ; i++ ){
            for( int j = 0 ; j < k ; j++ ){
                if( arr[i][j].equalsIgnoreCase("*") ){
                    row = i;
                    column = j;
                    break;
                }
            }
        }

        search_node temp_node;


        if( (row - 1) >= 0 ){

            String[][] up = new String[k][k] ;
            for (int i = 0; i < arr.length; i++) {
                System.arraycopy(arr[i], 0, up[i], 0, up[i].length);
            }

            up[row-1][column] = arr[row][column];
            up[row][column] = arr[row-1][column];
            temp_node = new search_node(curr_node.getMoves() + 1, up, curr_node);
            if( !checked(temp_node) ){
                pq.add(temp_node);
            }
        }


        if( (row + 1) < k ){

            String[][] down = new String[k][k];
            for (int i = 0; i < arr.length; i++) {
                System.arraycopy(arr[i], 0, down[i], 0, down[i].length);
            }

            down[row+1][column] = arr[row][column];
            down[row][column] = arr[row+1][column];
            temp_node = new search_node(curr_node.getMoves() + 1, down, curr_node);
            if( !checked(temp_node) ){
                pq.add(temp_node);
            }
        }

        if( (column - 1) >= 0 ){

            String[][] right = new String[k][k];
            for (int i = 0; i < arr.length; i++) {
                System.arraycopy(arr[i], 0, right[i], 0, right[i].length);
            }

            right[row][column-1] = arr[row][column];
            right[row][column] = arr[row][column-1];
            temp_node = new search_node(curr_node.getMoves() + 1, right, curr_node);
            if( !checked(temp_node) ){
                pq.add(temp_node);
            }
        }

        if( (column + 1) < k ){
            String[][] left = new String[k][k];
            for (int i = 0; i < arr.length; i++) {
                System.arraycopy(arr[i], 0, left[i], 0, left[i].length);
            }

            left[row][column + 1] = arr[row][column];
            left[row][column] = arr[row][column + 1];
            temp_node = new search_node(curr_node.getMoves() + 1, left, curr_node);
            if( !checked(temp_node) ){
                pq.add(temp_node);
            }
        }

        return pq;
    }

    public static boolean reached_goal(String[][] arr, int k){
        int value;
        for(int i = 0 ; i < k ; i++ ){
            for( int j = 0 ; j < k ; j++ ){
                if( arr[i][j].equalsIgnoreCase("*")){
                    if( (i != (k - 1) ) | (j != ( k - 1) ) ){
                        return false;
                    }
                    continue;
                }
                value = Integer.parseInt(arr[i][j]);
                Pair pair = ideal.get(value);
                if(  ( pair.getColumn() != j ) | ( pair.getRow() != i )  ){
                    return false;
                }
            }
        }
        return true;
    }

    public static void main(String[] args) throws FileNotFoundException {

        Scanner sc = new Scanner(new BufferedReader(new FileReader("input.txt")));
        int k = Integer.parseInt( sc.nextLine() );
        String[][] arr = new String[k][k];
        while(sc.hasNextLine()) {
            for (int i=0; i<arr.length; i++) {
                String[] line = sc.nextLine().trim().split(" ");
                for (int j=0; j<line.length; j++) {
                    arr[i][j] = line[j];
                }
            }
        }
        boolean solve = check_solvability(arr, k);
        if(solve == false){
            System.out.println("Board not solvable");
            return;
        }
        System.out.println("Board solvable");
        store_ideal(k);

        search_node initial = new search_node(0, arr, null);
        search_node temp = initial;
        // Hamming Distance
        open_list_1.add(initial);
        while( !open_list_1.isEmpty() ){
            temp = open_list_1.poll();
            close_list.put(temp.toString(), temp);
            boolean reached = reached_goal(temp.getBoard(), k);
            if( reached == true ){
                break;
            }

            open_list_1 = get_neighbours(open_list_1, temp, k);
        }
        System.out.println("Hamming Distance : ");
        search_node output = temp;

        System.out.println("Optimal Cost : " + output.getMoves());
        System.out.println("Expanded Nodes : " + close_list.size() );
        System.out.println("Explored Nodes : " +  + open_list_1.size() + close_list.size() );
        print_boards(output);
        close_list = null;
        open_list_1 = null;

        // Manhattan distance
        open_list_2.add(initial);
        temp = initial;
        close_list = new HashMap<String, search_node>();
        while( !open_list_2.isEmpty() ){
            temp = open_list_2.poll();
            close_list.put(temp.toString(), temp);
            boolean reached = reached_goal(temp.getBoard(), k);
            if( reached == true ){
                break;
            }
            open_list_2 = get_neighbours(open_list_2, temp, k);
        }
        System.out.println("Manhattan Distance : ");
        output = temp;

        System.out.println("Optimal Cost : " + output.getMoves());
        System.out.println("Expanded Nodes : " + close_list.size() );
        System.out.println("Explored Nodes : " + open_list_2.size() + close_list.size() );
        print_boards(output);
        close_list = null;
        open_list_2 = null;

        // Linear distance
        open_list_3.add(initial);
        temp = initial;
        close_list = new HashMap<String, search_node>();

        while( !open_list_3.isEmpty() ){
            temp = open_list_3.poll();
            close_list.put(temp.toString(), temp);
            boolean reached = reached_goal(temp.getBoard(), k);
            if( reached == true ){
                break;
            }
            open_list_3 = get_neighbours(open_list_3, temp, k);
        }
        System.out.println("Linear Conflict Distance : ");
        output = temp;

        System.out.println("Optimal Cost : " + output.getMoves());
        System.out.println("Expanded Nodes : " + close_list.size() );
        System.out.println("Explored Nodes : " + open_list_3.size() + close_list.size() );
        print_boards(output);
        close_list = null;
        open_list_3 = null;

    }
}
