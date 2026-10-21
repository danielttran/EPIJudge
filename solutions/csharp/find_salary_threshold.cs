public class Solution
{
    public double FindSalaryCap(int target_payroll, List<int> current_salaries)
    {
        var salaries = current_salaries.Order().ToArray();
        long paid = 0;
        for (int i = 0; i < salaries.Length; i++)
        {
            double cap = (target_payroll - paid) / (double)(salaries.Length - i);
            if (cap <= salaries[i])
                return cap;
            paid += salaries[i];
        }
        return paid == target_payroll && salaries.Length > 0 ? salaries[^1] : -1;
    }
}
