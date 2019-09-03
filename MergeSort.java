import java.io.*;
import java.util.*;


class Solution {
  public static void main(String[] args) {
    int arr[] = new int[] {12,1,5,7,31,62,3,19};
    int mergedArr[] = mergeSort(arr, 0, arr.length-1);
    for(int i=0; i<mergedArr.length; i++) {
      System.out.print(mergedArr[i] + " ");
    }
  }
  
  static int[] merge(int Arr[], int start, int mid, int end) {
  // create a temp array
  int temp[] = new int[end - start + 1];
  
  // crawlers for both intervals and for temp
  int i = start, j = mid+1, k = 0;

  // traverse both arrays and in each iteration add smaller of both elements in temp 
  while(i <= mid && j <= end) {
    if(Arr[i] <= Arr[j]) {
      temp[k] = Arr[i];
      k += 1; i += 1;
    }
    else {
      temp[k] = Arr[j];
      k += 1; j += 1;
    }
  }
  
  // add elements left in the first interval 
  while(i <= mid) {
    temp[k] = Arr[i];
    k += 1; i += 1;
  }

  // add elements left in the second interval 
  while(j <= end) {
    temp[k] = Arr[j];
    k += 1; j += 1;
  }

  // copy temp to original interval
  for(i = start; i <= end; i += 1) {
    Arr[i] = temp[i - start];
  }
    return Arr;
}

// Arr is an array of integer type
// start and end are the starting and ending index of current interval of Arr

static int[] mergeSort(int Arr[], int start, int end) {

  System.out.println( "Start : " + start + " end : "+ end);
  
  if(start < end) {
    int mid = (start + end) / 2;
    
    System.out.println( "mid : " + mid);
                       
    mergeSort(Arr, start, mid);
    
    System.out.println( "Start and end are same here");
    
    mergeSort(Arr, mid+1, end);
    
    System.out.println( "Mid and end are same here");
    
    int[] Arr2 = merge(Arr, start, mid, end);
    System.out.println( "Merge done here : " + start +" "+ mid +" "+ end);
    for(int i=0;i<Arr2.length; i++){
      System.out.println( "Merged List : " + Arr2[i]);
    }
    
  }
  return Arr;
}
  
}
